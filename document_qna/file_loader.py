import os
# from unstructured.partition.auto import partition
import textract

# nltk.download('punkt')

def read_file(file_path):
    # Read a file using Unstructured library.
    text = textract.process(file_path)
    # Process elements as needed, e.g., extract text
    return text


# def read_file(file_path):
#     # Read a file using Unstructured library.
#     elements = partition(filename=file_path)
#     # Process elements as needed, e.g., extract text
#     return ' '.join([el.text for el in elements])

def read_directory(directory_path, recursive=True):
    # Recursively traverse directory and read files.
    documents = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                content = read_file(file_path)
                documents.append(content)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

        if not recursive:
            break  # Don't process subdirectories if recursive is False

    return documents
