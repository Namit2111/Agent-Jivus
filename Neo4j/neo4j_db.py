import os
import ast
import re
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "namitjain12"  
driver = GraphDatabase.driver(uri, auth=(username, password))

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
        
        pattern = re.compile(r'(?:from\s+(\S+)\s+import\s+(\S+))|(?:import\s+(\S+))')
        matches = pattern.findall(content)
        for match in matches:
            if match[1]:  
                imports.append((match[0], match[1]))
            elif match[2]:  
                imports.append((match[2], None)) 

def scan_directory(root_folder):
    """Scan the directory, extract functions, and create the graph."""
    for folder_name, subfolders, filenames in os.walk(root_folder):
      
        parent_folder = os.path.basename(root_folder) 

      
        with driver.session() as session:
            session.write_transaction(create_folder, parent_folder)

        folder_name_in_db = os.path.basename(folder_name)
        with driver.session() as session:
            session.write_transaction(create_folder, folder_name_in_db, parent_folder)

        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(folder_name, filename)
                file_name = filename

                with driver.session() as session:
                    session.write_transaction(create_file, file_name, folder_name_in_db)

                functions = get_functions_from_file(file_path)
                for func in functions:
                    with driver.session() as session:
                        session.write_transaction(create_function, func, file_name, folder_name_in_db)

             
                function_calls = get_function_calls(file_path)
                for callee_func in function_calls:
                  
                    for caller_func in functions:
                        if caller_func != callee_func:  
                            with driver.session() as session:
                                session.write_transaction(create_function_call, caller_func, callee_func, file_name, filename)
             
                imports = get_imports_from_file(file_path)
                for imported_file, imported_func in imports:
                    
                    with driver.session() as session:
                        if imported_func:
                            
                            session.write_transaction(create_import, file_name, imported_func, imported_file)
                        else:
                            
                            session.write_transaction(create_import, file_name, "module", imported_file)

scan_directory("RAG")
