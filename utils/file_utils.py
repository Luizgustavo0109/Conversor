import os 

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1]