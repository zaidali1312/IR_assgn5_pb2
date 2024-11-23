import os

def load_documents(data_dir):
    """
    Load all text files from the given directory and return a list of file contents.
    """
    documents = []
    file_names = []
    
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".txt"):  # Only process .txt files
            file_path = os.path.join(data_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                documents.append(file.read())
                file_names.append(file_name)
    
    return documents, file_names
