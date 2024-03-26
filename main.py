import os
import datetime

# Hardcoded folder location
FOLDER_LOCATION = "/path/to/your/folder"

# Dictionary to store file information
file_info = {}

def commit_snapshot():
    """Update snapshot time to current time."""
    snapshot_time = datetime.datetime.now()
    print("Snapshot updated to:", snapshot_time)

def get_file_info(filename):
    """Print general information about the file."""
    if filename not in file_info:
        print("File not found.")
        return
    
    info = file_info[filename]
    print("Filename:", filename)
    print("Extension:", info['extension'])
    print("Created:", info['created'])
    print("Updated:", info['updated'])

    if info['extension'] in ['.png', '.jpg']:
        print("Image Size:", info['image_size'])
    elif info['extension'] == '.txt':
        print("Line Count:", info['line_count'])
        print("Word Count:", info['word_count'])
        print("Character Count:", info['char_count'])
    elif info['extension'] in ['.py', '.java']:
        print("Line Count:", info['line_count'])
        print("Class Count:", info['class_count'])
        print("Method Count:", info['method_count'])

def get_all_files_info():
    """Print information about all files."""
    for filename, info in file_info.items():
        print("Filename:", filename)
        print("Extension:", info['extension'])
        print("Created:", info['created'])
        print("Updated:", info['updated'])

        if info['extension'] in ['.png', '.jpg']:
            print("Image Size:", info['image_size'])
        elif info['extension'] == '.txt':
            print("Line Count:", info['line_count'])
            print("Word Count:", info['word_count'])
            print("Character Count:", info['char_count'])
        elif info['extension'] in ['.py', '.java']:
            print("Line Count:", info['line_count'])
            print("Class Count:", info['class_count'])
            print("Method Count:", info['method_count'])
        print()

def update_file_info():
    """Update information about all files in the folder."""
    global file_info
    file_info = {}
    for filename in os.listdir(FOLDER_LOCATION):
        filepath = os.path.join(FOLDER_LOCATION, filename)
        if os.path.isfile(filepath):
            file_stats = os.stat(filepath)
            created_time = datetime.datetime.fromtimestamp(file_stats.st_ctime)
            updated_time = datetime.datetime.fromtimestamp(file_stats.st_mtime)
            extension = os.path.splitext(filename)[1]

            if extension in ['.png', '.jpg']:
                image_size = f"{file_stats.st_size} bytes"
            elif extension == '.txt':
                with open(filepath, 'r') as file:
                    line_count = sum(1 for line in file)
                    file.seek(0)
                    word_count = len(file.read().split())
                    file.seek(0)
                    char_count = len(file.read())
            elif extension in ['.py', '.java']:
                with open(filepath, 'r') as file:
                    line_count = sum(1 for line in file)
                    file.seek(0)
                    class_count = 0
                    method_count = 0
                    for line in file:
                        if line.strip().startswith('class '):
                            class_count += 1
                        elif line.strip().startswith('def '):
                            method_count += 1
            
            file_info[filename] = {
                'extension': extension,
                'created': created_time,
                'updated': updated_time,
                'image_size': image_size if extension in ['.png', '.jpg'] else None,
                'line_count': line_count if extension in ['.txt', '.py', '.java'] else None,
                'word_count': word_count if extension == '.txt' else None,
                'char_count': char_count if extension == '.txt' else None,
                'class_count': class_count if extension in ['.py', '.java'] else None,
                'method_count': method_count if extension in ['.py', '.java'] else None
            }

def status():
    """Show changes in files since the last snapshot."""
    for filename, info in file_info.items():
        updated_since_snapshot = info['updated'] > snapshot_time
        print(f"{filename} {'changed' if updated_since_snapshot else 'not changed'} since last snapshot")

# Initial update of file information
update_file_info()

while True:
    command = input("Enter command (commit/info <filename>/all files/status): ").strip()
    if command.startswith("info"):
        filename = command.split(maxsplit=1)[1]
        get_file_info(filename)
    elif command == "all files":
        get_all_files_info()
    elif command == "commit":
        commit_snapshot()
        update_file_info()
    elif command == "status":
        status()
    else:
        print("Invalid command.")
