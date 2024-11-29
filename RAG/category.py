# from flask import Flask, request, jsonify
from pymongo import MongoClient
from summarizer_groq import llama_chat,llama_chat_json
import json
# app = Flask(__name__)
client = MongoClient('mongodb+srv://sagar:eda6XT4A4bU9ua6D@perfectsprout-dev-qa-te.jorx2nm.mongodb.net/?retryWrites=true&w=majority')
db = client['test'] 
collection = db['categorized_product_info']   



# @app.route("/check-availability", methods=["POST"])
def check_availability():
    # data = request.get_json()
    data = {
    "message": {
        "toolCalls": [
            {
                "id": "12345", 
                "function": {
                    "arguments": {
                        "categories": ["Company_overview", "Testimonials"],
                        "conversation": "bot: I have called to tell you about SmartHealth Tracker Pro.\nuser: What does the product do?\nbot: It is a health tracker app that allows you to track your health and fitness goals.\nuser: Can I get company overview?"
                    }
                }
            }
        ]
    }
}

    categories = data['message']['toolCalls'][0]['function']['arguments'].get('categories')
    conversation = data['message']['toolCalls'][0]['function']['arguments'].get('conversation')
    tool_calls = data.get('message', {}).get('toolCalls', [])
    tool_call_id = tool_calls[0].get('id', None) if tool_calls else ""
    # -------------------------------------------------------- for testing -------------------------------------------
    # categories = data.get('category')
    # conversation = data.get('conversation')
    # categories = ["Company_overview","Testimonials"]
    # conversation = ''' 
    # bot:I have called to tell you about smart health tracker pro.
    # user: what deos the product do?
    # bot: It is a health tracker app that allows you to track your health and fitness goals.
    # user: can i get company overview?
    # '''
    
    unique_pair = {"product_name": "SmartHealth Tracker Pro"} # change it with some unique pair like product ID
    result = collection.find_one(unique_pair) 
    # print(collection)

    if result:
        material = result.get('categories')

        meta_desciption = {key:value['meta']['description'] for key,value in material.items() if key in categories}

        res = llama_chat_json(prompt="Given categories and their descriptions are: {} and the conversation is: {}. Choose which category is related to the conversation and return in the json format:follow this schema in every condition, key will always be the word type and value will always be the chosen category name. '{{type: chosen category name}}' . Remeber to choose only one category and follow the json format".format(meta_desciption, conversation))
        
        category = json.loads(res)['type']
        category_data = {key:value['data'] for key,value in material.items() if key in category}
     
        summary = llama_chat(prompt="using the given category and its data: {} and the conversation is: {}.  Generate a summary in 10-15 lines of categroy data . Summary should be oriented towards the conversation.".format(category_data, conversation))
        response_value = {
        "results": [
            {
                "toolCallId": tool_call_id,
                "result": summary
            }
        ]
    }
        return response_value
        # print(f"Material for category '{category}': {material}")
        # return jsonify({"status": "success", "material": material}), 200
    else:
        response_value={
            "results": [
                {
                    "toolCallId": tool_call_id,
                    "result": "Category not found"
                }
            ]
        }
        # print(f"Category '{category}' not found.")
        return response_value
        # return jsonify({"status": "error", "message": "Category not found"}), 404

# if __name__ == "__main__":
#     app.run(debug=True)
print(check_availability())