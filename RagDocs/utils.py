import os
import google.generativeai as genai
import time
genai.configure(api_key="")

model = genai.GenerativeModel("gemini-1.5-flash")


def find_python_files(root_folder, skip_folders=None):

    if skip_folders is None:
        skip_folders = set()
    

    python_files = []
    

    for dirpath, dirnames, filenames in os.walk(root_folder):
     
        dirnames[:] = [d for d in dirnames if d not in skip_folders]
        
   
        for file in filenames:
            if file.endswith('.py'):
                python_files.append(os.path.join(dirpath, file))
    
    return python_files


def read_file(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        content = file.read()
    return content

def generate_documentation(file_content):
    response = model.generate_content("Given file content of a python file write a documentation of this file in markdown format content:{}".format(file_content) )
    return response.text

def write_documentation(file_path, documentation):
    markdown_file_path = os.path.splitext(file_path)[0] + ".md"
    with open(markdown_file_path, 'w') as file:
        file.write(documentation)

if __name__ == "__main__":
# Example usage:
    root_folder = 'src'
    skip_folders = {'live_call', 'post_call'}
    python_files = find_python_files(root_folder, skip_folders)

    # Print the found Python files
    for py_file in python_files:
        print(py_file)
