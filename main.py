import os
import datetime

folder_path = "/path/to/your/folder"

def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1]
    created_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    updated_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    return file_name, file_extension, created_time, updated_time

def get_image_info(file_path):
    import PIL.Image
    with PIL.Image.open(file_path) as img:
        width, height = img.size
    return f"{width}x{height}"

def get_text_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        line_count = len(lines)
        word_count = sum(len(line.split()) for line in lines)
        char_count = sum(len(line) for line in lines)
    return line_count, word_count, char_count

def get_program_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        line_count = len(lines)
        class_count = sum(1 for line in lines if line.strip().startswith("class "))
        method_count = sum(1 for line in lines if line.strip().startswith("def "))
    return line_count, class_count, method_count

def main():
    while True:
        action = input("Enter action (commit/info <filename>/status): ").split()

        if action[0] == "commit":
            snapshot_time = datetime.datetime.now()
            print(f"Snapshot time updated to: {snapshot_time}")

        elif action[0] == "info":
            if len(action) != 2:
                print("Invalid command. Please provide filename.")
                continue
            file_name = action[1]
            file_path = os.path.join(folder_path, file_name)
            if not os.path.exists(file_path):
                print("File not found.")
                continue
            file_info = get_file_info(file_path)
            file_extension = file_info[1]
            if file_extension in ['.png', '.jpg']:
                print(f"Image Size: {get_image_info(file_path)}")
            elif file_extension == '.txt':
                text_info = get_text_info(file_path)
                print(f"Line count: {text_info[0]}")
                print(f"Word count: {text_info[1]}")
                print(f"Character count: {text_info[2]}")
            elif file_extension in ['.py', '.java']:
                program_info = get_program_info(file_path)
                print(f"Line count: {program_info[0]}")
                print(f"Class count: {program_info[1]}")
                print(f"Method count: {program_info[2]}")
            else:
                print("Unknown file type.")

        elif action[0] == "status":
            snapshot_time = datetime.datetime.now()
            print(f"Snapshot time: {snapshot_time}")
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    file_info = get_file_info(file_path)
                    if file_info[3] > snapshot_time:
                        print(f"{file_info[0]} has been changed since snapshot time.")

        else:
            print("Invalid action.")

if __name__ == "__main__":
    main()
