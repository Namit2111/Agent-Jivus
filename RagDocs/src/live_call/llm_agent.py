import asyncio
import json
import openai
from src.config import config
from src.db.models import Prompts
from src.db.schemas import Conversation
from src.db.subroutes.live_insights import update_live_insight
from src.db.subroutes.transcripts import patch_transcript
from aio_pika import connect, Message, ExchangeType

from src.enums import CallTypes
from src.live_call.enums import InsightHandling
from src.logger import Logger
from src.utils.prompt_formatter import PromptTemplate
from src.utils.prompts import get_prompt


class LLMAgent:
    def __init__(
        self,
        api_key: str,
        conversation: Conversation,
        logger_name: str = "llm_agent",
        model: str = "gpt-4-0125-preview",
        alt_insight_pipeline: bool = False,
        stream_output: bool = True,
        ignore_agent_transcriptions=False,
        previous_insight_handling=InsightHandling.INTERRUPT,
    ):
        """
        LLMAgent Class.

        Args:
            api_key (str): OpenAI API Key
            conversation (Conversation, optional): Conversation Object.
            logger_name (str, optional): Logger Name. Defaults to "llm_agent_logger".
            model (str, optional): Name of the OpenAI Model to use. Defaults to "gpt-4-0613".
            alt_insight_pipeline (bool, optional): Alternate Insight generation pipeline. If set to true this class sends pair of insights to the model. Defaults to False.
        """
        self.api_key = api_key
        self.model = model
        self.logger = Logger(logger_name)
        self.conversation = conversation
        self.insights = []
        self.transcript = {}
        self.stored_transcript = {}
        self.stored_insight_content = ""
        self.rmq_url = config["RABBITMQ_URL"]
        self.rmq_name = "insight_queue"
        self.alt_insight_pipeline = alt_insight_pipeline
        self.stream_output = stream_output
        self.turn_counter = 0
        if ignore_agent_transcriptions and self.alt_insight_pipeline:
            raise ValueError(
                "`ignore_agent_transcriptions` and `alt_insight_pipeline cannot` both be true."
            )
        self.ignore_agent_transcriptions = ignore_agent_transcriptions
        self.previous_insight_handling = previous_insight_handling

        openai.api_key = self.api_key

    def __get_system_prompt(self):
        self.sys_prompt = get_prompt(
            promptType="insight",
            callType=CallTypes.LIVE_CALL,
            defaultPromptFile="live_call_insight_prompt.txt",
        )

        self.sys_prompt = PromptTemplate(self.sys_prompt)

        try:
            productPitch = self.conversation.profileInfo.productInfo.summary  # type: ignore
        except:
            productPitch = "No Product Pitch"

        try:
            prospectName = self.conversation.profileInfo.linkedinInfo.data["full_name"]  # type: ignore
        except:
            prospectName = "No Prospect Name"

        try:
            prospectDesignation = self.conversation.profileInfo.linkedinInfo.data["experiences"][0]["title"]  # type: ignore
        except:
            prospectDesignation = "No Prospect Designation"

        try:
            companyIndustry = self.conversation.profileInfo.linkedinInfo.data["experiences"][0]["company"]  # type: ignore
        except:
            companyIndustry = "No Company"

        try:
            linkedinSummary = self.conversation.profileInfo.linkedinInfo.summary  # type: ignore
        except:
            linkedinSummary = "No Linkedin Summary"

        try:
            emailChain = self.conversation.profileInfo.hubspotInfo.email_chain  # type: ignore
        except:
            emailChain = "No Emails"

        try:
            notes = self.conversation.profileInfo.hubspotInfo.notes  # type: ignore
        except:
            notes = "No Notes"

        callScenario = "Discovery call"

        try:
            desiredOutcome = self.conversation.metadata["desiredOutcome"]  # type: ignore
        except:
            desiredOutcome = "No Desired Outcome"

        self.sys_prompt = self.sys_prompt.fill_slots(
            {
                "Product Pitch": productPitch,
                "Prospect Name": prospectName,
                "Prospect Designation": prospectDesignation,
                "Company Industry": companyIndustry,
                "Call Scenario": callScenario,
                "Linkedin Summary": linkedinSummary,
                "Email Chain": emailChain,
                "Notes": notes,
                "Desired Outcome": desiredOutcome,
            }
        )

        self.logger.debug("sys_prompt: {}".format(self.sys_prompt))

    async def __insight_create_rabbitmq_channel(self, rabbitmq_url: str):
        self.logger.debug("Creating rabbitmq channel for insight generation")

        # Create a connection
        connection = await connect(rabbitmq_url)

        # Creating a channel
        channel = await connection.channel()

        self.logger.info("RabbitMQ channel created.")
        return connection, channel

    async def __insight_send_json_to_queue(self, message):
        message_bytes = json.dumps(message).encode("utf-8")

        # Sending the message
        await self.rmq_exchange.publish(
            Message(message_bytes),
            routing_key=f"insight_{str(self.conversation.conversationId)}",
        )

    async def __insight_create_queue(self, channel, queue_name="insight_queue"):
        self.logger.debug("Creating rabbitmq queue for insight generation")

        try:
            self.rmq_exchange = await channel.declare_exchange(
                "live_call_agent", ExchangeType.DIRECT, durable=False, auto_delete=True
            )
        except Exception as e:
            self.logger.error(f"Failed to declare exchange 'live_call_agent': {e}")
            raise  # re-raise the exception
        else:
            self.logger.debug(f"Exchange 'live_call_agent' declared.")

        # Declare a queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        self.logger.debug(f"Queue '{queue_name}' declared.")

        # Bind the queue to the exchange with the routing key
        await queue.bind(
            self.rmq_exchange, routing_key=f"insight_{self.conversation.conversationId}"
        )

        self.logger.info(
            f"Queue '{queue_name}' bound to exchange 'live_call_agent' with routing key 'insight_{self.conversation.conversationId}'."
        )
        return queue

    async def start_conversation(self, agent_name="agent"):
        """
        Used to initialize a conversation.

        Args:
            agent_name (str, optional): Name of the agent expected from `transcript['speaker']` for agent turns. Defaults to `agent`.
            ignore_agent_transcriptions (bool, optional): If set to `true`, the agent transcriptions are not sent to LLM Agent. Cannot be set to `True` if `alt_insight_pipeline` is set to `True`. Defaults to `False`.

        Returns:
            conversation_id
        """
        self.logger.debug("Inside start_conversation")
        self.__get_system_prompt()

        sys_msg = {"role": "system", "content": self.sys_prompt}
        self.messages = [sys_msg]
        self.insights = []
        self.agent_name = agent_name

        (
            self.rmq_connection,
            self.rmq_channel,
        ) = await self.__insight_create_rabbitmq_channel(self.rmq_url)
        self.rmq_queue = await self.__insight_create_queue(
            self.rmq_channel, self.rmq_name
        )
        self.logger.info("setup completed for LLM Agent")
        await self.__send_messages()
        return self.conversation.conversationId

    async def __send_insight(self, assistant_message):
        self.insights.append(assistant_message)

        if not self.stream_output:
            self.messages.append({"role": "assistant", "content": assistant_message})
            update_live_insight(
                self.conversation.conversationId,
                {
                    "nudge": assistant_message,
                    "time": self.transcript.get("end", "0"),
                    "turn_id": str(self.turn_counter),
                },
            )
        await self.__insight_send_json_to_queue(
            {
                "role": self.transcript.get(
                    "speaker", "system (No transcript speaker)"
                ),
                "nudge": assistant_message,
                "turn_id": str(self.turn_counter),
            }
        )

    async def __send_messages(self):
        self.logger.start_latency_timer()
        if self.stream_output:
            try:
                # Message to Frontend to set status to "generating"
                await self.__insight_send_json_to_queue(
                    {
                        "role": "system",
                        "nudge": "generating",
                        "turn_id": str(self.turn_counter),
                    }
                )
                self.logger.debug(f"Messages sent to openAI: \n{self.messages}")
                stream = await openai.AsyncOpenAI(
                    api_key=self.api_key
                ).chat.completions.create(
                    model=self.model,
                    messages=self.messages,  # type: ignore
                    frequency_penalty=0.5,
                    presence_penalty=0.5,
                    max_tokens=200,
                    temperature=1.1,
                    stream=True,
                )
            except openai.OpenAIError as e:
                # Message to Frontend to set status to "error"
                await self.__insight_send_json_to_queue(
                    {
                        "role": "system",
                        "nudge": f"error: {e}",
                        "turn_id": str(self.turn_counter),
                    }
                )
                self.logger.error(f"An error occurred: {e}")
                return None

            full_message = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    assistant_message = chunk.choices[0].delta.content
                    full_message += assistant_message
                    await self.__send_insight(assistant_message)
            self.messages.append({"role": "assistant", "content": full_message})
            # Send full insight to DB
            update_live_insight(
                self.conversation.conversationId,
                {
                    "nudge": full_message,
                    "time": self.transcript.get("end", "0"),
                    "turn_id": str(self.turn_counter),
                    "role": self.transcript.get(
                        "speaker", "system (No transcript speaker)"
                    ),
                },
            )

            self.logger.debug(
                f"Insight inside the LLM Class for turn {str(self.turn_counter)}: {full_message}"
            )

            # Message to Frontend to set status to "analysing"
            await self.__insight_send_json_to_queue(
                {
                    "role": "system",
                    "nudge": "analysing",
                    "turn_id": str(self.turn_counter),
                }
            )
            self.logger.log_latency("Generated Full Insight")
            return None
        else:
            try:
                # Message to Frontend to set status to "generating"
                await self.__insight_send_json_to_queue(
                    {
                        "role": "system",
                        "nudge": "generating",
                        "turn_id": str(self.turn_counter),
                    }
                )
                self.logger.debug(f"Messages sent to openAI: \n{self.messages}")
                response = await openai.AsyncOpenAI(
                    api_key=self.api_key
                ).chat.completions.create(
                    model=self.model,
                    messages=self.messages,  # type: ignore
                    frequency_penalty=0.5,
                    presence_penalty=0.5,
                    max_tokens=200,
                    temperature=1.1,
                )
            except openai.OpenAIError as e:
                # Message to Frontend to set status to "error"
                await self.__insight_send_json_to_queue(
                    {
                        "role": "system",
                        "nudge": f"error: {e}",
                        "turn_id": str(self.turn_counter),
                    }
                )
                self.logger.error(f"An error occurred: {e}")
            assistant_message = response.choices[0].message.content
            await self.__send_insight(assistant_message)
            self.logger.debug(
                f"Insight inside the LLM Class for turn {str(self.turn_counter)}: {assistant_message}"
            )
            # Message to Frontend to set status to "analysing"
            await self.__insight_send_json_to_queue(
                {
                    "role": "system",
                    "nudge": "analysing",
                    "turn_id": str(self.turn_counter),
                }
            )
            self.logger.log_latency("Generated Full Insight")
            return None

    async def __generate_insight(self):
        self.logger.debug("Inside generate_insight")

        if self.ignore_agent_transcriptions:
            if self.transcript["speaker"] == self.agent_name:
                self.transcript = {}
                self.logger.debug(
                    "Exiting __generate_insight, coz `self.transcript['speaker'] == self.agent_name`"
                )
                return None

        if self.alt_insight_pipeline:
            if not self.stored_insight_content:
                self.stored_insight_content = (
                    f"{self.transcript['speaker']}: {self.transcript['transcript']}"
                )
                self.logger.debug(
                    "Exiting __generate_insight, coz `not self.stored_insight_content`"
                )
                return None
            else:
                if self.transcript["speaker"] != self.agent_name:
                    content = f"{self.stored_insight_content}\n{self.transcript['speaker']}: {self.transcript['transcript']}"
                    self.logger.debug(f"content: {content}")
                    self.messages.append({"role": "user", "content": content})
                    self.stored_insight_content = ""
                else:
                    self.stored_insight_content = f"{self.stored_insight_content}\n{self.transcript['speaker']}: {self.transcript['transcript']}"
                    self.logger.debug(
                        "Exiting __generate_insight, coz `self.transcript['speaker'] == self.agent_name`"
                    )
                    return None
        else:
            content = f"{self.transcript['speaker']}: {self.transcript['transcript']}"
            self.logger.debug(f"content: {content}")
            self.messages.append({"role": "user", "content": content})

        self.logger.debug(
            f"Transcript Inside generate_insight for turn {self.turn_counter}: {self.transcript}"
        )
        self.turn_counter = self.turn_counter + 1
        return await self.__send_messages()

    def __join_transcripts(self, old_transcript, new_transcript):
        return {
            "transcript": " ".join(
                [old_transcript["transcript"], new_transcript["transcript"]]
            ),
            "speaker": new_transcript.get("speaker", "No Speaker"),
            "start_time": old_transcript.get("start_time", 0.0),
            "end_time": new_transcript.get("end_time", 0.0),
        }

    # I wrote this Function, but turned out not to be useful. Keeping it here for future use-cases.
    async def __cancelable_sleep(self, delay: float):
        """just do self.sleep_task.cancel() to finish sleeping.

        Args:
            delay (float): _description_

        Returns:
            _type_: _description_
        """
        self.sleep_task = asyncio.ensure_future(asyncio.sleep(delay))
        try:
            self.logger.debug(f"Sleeping for {delay} seconds")
            return await self.sleep_task
        except asyncio.CancelledError:
            self.logger.debug(f"Sleeping canceled")
            return None

    async def __delayed_generate_insight(self, delay: float = 3) -> None:
        """Will trigger __generate_insight after provided delay. Will cancel insight generation if task canceled.

        Args:
            delay (float): _description_
        """
        generating_insight = False
        try:
            await asyncio.ensure_future(asyncio.sleep(delay))
            if self.stored_transcript:
                self.transcript = self.stored_transcript
                self.stored_transcript = {}
            generating_insight = True
            await self.__generate_insight()
            self.transcript = {}
            return None
        except asyncio.CancelledError:
            if generating_insight:
                self.messages.pop()
                await self.__send_insight(
                    " <Interrupted, generating insight from latest chat.>"
                )

                await self.__insight_send_json_to_queue(
                    {
                        "role": "system",
                        "nudge": "interrupted",
                        "turn_id": str(self.turn_counter),
                    }
                )
            return None

    async def ensure_previous_insight(self):
        try:
            while not self.insight_task.done():
                await asyncio.sleep(0.1)
            return None
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return None

    async def cancel_insight_task(self) -> None:
        try:
            if not self.insight_task.done():
                # TODO: Add a cancel cancellation for small/insignificant interrupting transcripts here.
                # Not solved by valid_transcript() coz we sometimes need small transcripts to come thru.
                status = self.insight_task.cancel()
                await self.insight_task
                self.logger.debug(f"insight_task canceled: {status}")
            return None
        except Exception as e:
            self.logger.error(f"Error canceling insight_task: {e}")
            return None

    def valid_transcript(self, transcript: dict) -> bool:
        min_transcript_length = 5
        if len(transcript["transcript"]) < min_transcript_length:
            return False
        else:
            return True

    async def add_new_transcript(
        self, transcript: dict, use_simplification: bool = True
    ):
        """Used for adding new transcript for model.

        Args:
            transcript (dict): Input Transcript.
            use_simplification (bool, optional): If true, combines consecutive transcripts if they have the same speaker. Defaults to True.

        Returns:
            _type_: _description_
        """

        if self.valid_transcript(transcript):
            pass
        else:
            self.logger.debug(
                f"Transcript not valid for insight generation: {transcript}"
            )
            return None

        if self.previous_insight_handling == InsightHandling.FINISH:
            await self.ensure_previous_insight()

        # Checks if previous iteration stored anything.
        if self.stored_transcript:
            self.transcript = self.stored_transcript
            self.stored_transcript = {}

        transcript["transcript"] = transcript["transcript"].strip()
        self.logger.debug(f"INSIDE add_new_transcript | transcript: {transcript}")

        # Ignore the whole turn if the transcript is empty
        if not transcript["transcript"]:
            self.logger.debug("Exiting add_new_transcript, coz empty transcript")
            return None

        patch_transcript(transcript, str(self.conversation.conversationId))  # type: ignore

        if use_simplification:
            if not self.transcript:
                self.transcript = transcript
                if self.previous_insight_handling == InsightHandling.INTERRUPT:
                    await self.cancel_insight_task()
                self.insight_task = asyncio.create_task(
                    self.__delayed_generate_insight()
                )
                return None
            # If consecutive transcript have the same speaker, they are combined.
            if self.transcript["speaker"] == transcript["speaker"]:
                self.transcript = self.__join_transcripts(self.transcript, transcript)
                if self.previous_insight_handling == InsightHandling.INTERRUPT:
                    await self.cancel_insight_task()
                self.insight_task = asyncio.create_task(
                    self.__delayed_generate_insight()
                )
                return None
            else:
                self.stored_transcript = transcript
                if self.previous_insight_handling == InsightHandling.INTERRUPT:
                    await self.cancel_insight_task()
                await self.__generate_insight()
                self.insight_task = (
                    asyncio.create_task(  # This is for the stored_transcript
                        self.__delayed_generate_insight()
                    )
                )
                self.logger.debug("Exiting add_new_transcript")
                return None

        else:
            self.transcript = transcript
            if self.previous_insight_handling == InsightHandling.INTERRUPT:
                await self.cancel_insight_task()
            await self.__generate_insight()
            self.logger.debug("Exiting add_new_transcript")
            return None
