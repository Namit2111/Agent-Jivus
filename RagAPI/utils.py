import os
import json
import time
from datetime import datetime
from config import ROOT_FOLDER, SKIP_FOLDERS, ALLOWED_EXTENSIONS, JSON_OUTPUT_FILE

import google.generativeai as genai

genai.configure(api_key="AIzaSyCAzHIdUXBpC627ff2QdWyLDLqDMFCNdrY")

model = genai.GenerativeModel("gemini-1.5-flash")

def find_files_with_extension(root_folder, skip_folders=None, allowed_extensions=None):
    if skip_folders is None:
        skip_folders = set()
    if allowed_extensions is None:
        allowed_extensions = {'.py'}

    files = []

    for dirpath, dirnames, filenames in os.walk(root_folder):
        dirnames[:] = [d for d in dirnames if d not in skip_folders]

        for file in filenames:
            if any(file.endswith(ext) for ext in allowed_extensions):
                files.append(os.path.join(dirpath, file))

    return files


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def generate_documentation(file_content):
    response = model.generate_content(f"""Given file content of a python file, write a documentation in markdown format
    doncumentation should be precise and concise including examples and response and api and call and other required to understand the code
    : {file_content}""")
    return response.text


def write_documentation(file_path, documentation):

    base_filename = os.path.splitext(file_path)[0] 
    file_extension = os.path.splitext(file_path)[1]  

    markdown_file_path = f"{base_filename}_{file_extension.lstrip('.')}.md"  

    with open(markdown_file_path, 'w') as file:
        file.write(documentation)


def update_json_file(file_path, json_data):
    with open(JSON_OUTPUT_FILE, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def track_file_update(file_path, json_data):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json_data[file_path] = timestamp
    update_json_file(file_path, json_data)


def load_json_data():
    if os.path.exists(JSON_OUTPUT_FILE):
        with open(JSON_OUTPUT_FILE, 'r') as json_file:
            return json.load(json_file)
    return {}


# if __name__ == "__main__":

#     python_files = find_files_with_extension(ROOT_FOLDER, skip_folders=SKIP_FOLDERS, allowed_extensions=ALLOWED_EXTENSIONS)
#     json_data = load_json_data()

#     for py_file in python_files:
#         print(py_file)
#         try:
#             content = read_file(py_file)
#             documentation = generate_documentation(content)
#             write_documentation(py_file, documentation)
#             print(f"Documentation written for: {py_file}")
#             track_file_update(py_file, json_data)
#         except Exception as e:
#             print(f"Failed to generate documentation for {py_file}: {e}")
