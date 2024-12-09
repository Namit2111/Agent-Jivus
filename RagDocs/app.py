from utils import find_files_with_extension, read_file, generate_documentation, write_documentation,track_file_update,load_json_data

from config import ROOT_FOLDER, SKIP_FOLDERS, ALLOWED_EXTENSIONS

def main():
    json_data = load_json_data()
    files = find_files_with_extension(root_folder=ROOT_FOLDER, skip_folders=SKIP_FOLDERS, allowed_extensions=ALLOWED_EXTENSIONS)
    
    for file in files:
        try:
            content = read_file(file_path=file)
            documentation = generate_documentation(file_content=content)
            write_documentation(file_path=file, documentation=documentation)
            print(f"Documentation written for: {file}")
            track_file_update(file_path=file, json_data=json_data)
        except:
            print(f"Failed to generate documentation for: {file}")

if __name__ == "__main__":
    main()
