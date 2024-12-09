import os
import ast
import re
from neo4j import GraphDatabase

# Neo4j connection setup
uri = "bolt://localhost:7687"  # Adjust if you're using a different URL or port
username = "neo4j"
password = "namitjain12"  # Set your Neo4j password here
driver = GraphDatabase.driver(uri, auth=(username, password))

# Initialize Neo4j session
def create_folder(tx, folder_name, parent_name=None):
    """Create a Folder node and link it to its parent if provided."""
    tx.run("""
        MERGE (f:Folder {name: $folder_name})
        """, folder_name=folder_name)

    if parent_name:
        tx.run("""
            MATCH (parent:Folder {name: $parent_name})
            MATCH (f:Folder {name: $folder_name})
            MERGE (parent)-[:CONTAINS]->(f)
            """, parent_name=parent_name, folder_name=folder_name)

def create_file(tx, file_name, folder_name):
    """Create a File node and link it to the Folder."""
    tx.run("""
        MATCH (f:Folder {name: $folder_name})
        MERGE (file:File {name: $file_name})
        MERGE (f)-[:CONTAINS]->(file)
        """, folder_name=folder_name, file_name=file_name)

def create_function(tx, function_name, file_name, folder_name):
    """Create a Function node and link it to its File."""
    tx.run("""
        MATCH (f:Folder {name: $folder_name})
        MATCH (file:File {name: $file_name})
        MERGE (func:Function {name: $function_name})
        MERGE (file)-[:HAS_FUNCTION]->(func)
        """, folder_name=folder_name, file_name=file_name, function_name=function_name)

def create_function_call(tx, caller_func, callee_func, caller_file, callee_file):
    """Create a CALLS relationship between two functions."""
    tx.run("""
        MATCH (caller:Function {name: $caller_func})
        MATCH (callee:Function {name: $callee_func})
        MATCH (caller_file:File {name: $caller_file})
        MATCH (callee_file:File {name: $callee_file})
        MERGE (caller)-[:CALLS]->(callee)
        """, caller_func=caller_func, callee_func=callee_func, caller_file=caller_file, callee_file=callee_file)

def create_import(tx, file_name, function_name, imported_file):
    """Create an IMPORTS relationship between a file and an imported function."""
    tx.run("""
        MATCH (file:File {name: $file_name})
        MATCH (imported_func:Function {name: $function_name})
        MATCH (imported_file:File {name: $imported_file})
        MERGE (file)-[:IMPORTS]->(imported_func)
        """, file_name=file_name, function_name=function_name, imported_file=imported_file)

def get_functions_from_file(file_path):
    """Extract function names from a Python file."""
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def get_function_calls(file_path):
    """Extract function calls from a Python file."""
    calls = []
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
    return calls

def get_imports_from_file(file_path):
    """Extract function imports from a Python file."""
    imports = []
    with open(file_path, "r") as file:
        content = file.read()
        # Match function imports like "from module import func" or "import module"
        pattern = re.compile(r'(?:from\s+(\S+)\s+import\s+(\S+))|(?:import\s+(\S+))')
        matches = pattern.findall(content)
        for match in matches:
            if match[1]:  # From-import
                imports.append((match[0], match[1]))
            elif match[2]:  # Regular import (like `import module`)
                imports.append((match[2], None))  # No specific function
    return imports

def scan_directory(root_folder):
    """Scan the directory, extract functions, and create the graph."""
    for folder_name, subfolders, filenames in os.walk(root_folder):
        # Determine parent folder
        parent_folder = os.path.basename(root_folder)  # For RAG, this will be 'RAG'

        # Create the parent folder (RAG)
        with driver.session() as session:
            session.write_transaction(create_folder, parent_folder)

        # Create current folder and connect it to its parent folder (RAG or subfolder)
        folder_name_in_db = os.path.basename(folder_name)
        with driver.session() as session:
            session.write_transaction(create_folder, folder_name_in_db, parent_folder)

        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(folder_name, filename)
                file_name = filename

                # Create File node and link to the Folder
                with driver.session() as session:
                    session.write_transaction(create_file, file_name, folder_name_in_db)

                # Extract functions from the Python file
                functions = get_functions_from_file(file_path)
                for func in functions:
                    with driver.session() as session:
                        session.write_transaction(create_function, func, file_name, folder_name_in_db)

                # Detect function calls and create relationships
                function_calls = get_function_calls(file_path)
                for callee_func in function_calls:
                    # If the file is calling functions from another file, create relationships
                    for caller_func in functions:
                        if caller_func != callee_func:  # Avoid self-calls
                            with driver.session() as session:
                                session.write_transaction(create_function_call, caller_func, callee_func, file_name, filename)

                # Extract imports (functions being imported from other files)
                imports = get_imports_from_file(file_path)
                for imported_file, imported_func in imports:
                    # Create relationship between importing file and imported function
                    with driver.session() as session:
                        if imported_func:
                            # Importing specific function
                            session.write_transaction(create_import, file_name, imported_func, imported_file)
                        else:
                            # Importing an entire module (no specific function)
                            session.write_transaction(create_import, file_name, "module", imported_file)

# Start scanning the "RAG" folder
scan_directory("RAG")
