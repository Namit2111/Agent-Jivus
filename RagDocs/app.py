from utils import find_python_files,read_file,generate_documentation,write_documentation

def main(root_folder, skip_folders):
    files = find_python_files(root_folder=root_folder, skip_folders=skip_folders)
    
    for file in files:
        try:
            content = read_file(file_path=file)
            documentation = generate_documentation(file_content=content)
            write_documentation(file_path=file, documentation=documentation)
            print(f"Documentation written for: {file}")
        except:
            print(f"Failed to generate documentation for: {file}")

if __name__ == "__main__":
    main(root_folder='src', skip_folders={'live_call', 'post_call'})