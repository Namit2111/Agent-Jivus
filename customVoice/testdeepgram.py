import os
from deepgram import DeepgramClient, SpeakOptions
from pydub import AudioSegment
import sys
import io
# Define the text and output file
# SPEAK_TEXT = {"text": "Hello, how can I help you today?"}
OUTPUT_FILENAME = "response.mp3"

def convert_to_mp3(text):
    SPEAK_TEXT = {"text": text}
    try:
        # STEP 1: Get API Key from environment variables
        api_key = ""
        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable is not set")

        # STEP 2: Create a Deepgram client
        deepgram = DeepgramClient(api_key)

        # STEP 3: Configure SpeakOptions
        options = SpeakOptions(
            model="aura-asteria-en",  # Ensure this model is available in your Deepgram account
            encoding="mp3",          # Specify audio encoding
        )

        # STEP 4: Generate and save the audio file
        response = deepgram.speak.rest.v("1").save(OUTPUT_FILENAME, SPEAK_TEXT, options)

        # STEP 5: Print response as JSON
        print("Audio successfully generated and saved!")
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")





if __name__ == "__main__":
    main()
