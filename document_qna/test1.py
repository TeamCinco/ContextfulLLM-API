import os
import configparser
from file_loader import read_directory

config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), 'settings.ini')
print(f"Config path: {config_path}")
print(f"File exists: {os.path.exists(config_path)}")



config.read(config_path)
print("Keys:", list(config.keys()))
print("Sections:", config.sections())


try:
    documents_path = config["storage"]["documents_path"]
    print(f"Documents path: {documents_path}")
except KeyError as e:
    print(f"KeyError occurred: {e}")
    print("Config contents:")
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config[section].items():
            print(f"{key} = {value}")
            
        # Storage
# documents_path = os.path.join(os.getcwd(), '..', config["storage"]["documents_path"] )
documents_path = os.path.join(os.getcwd(), config["storage"]["documents_path"] )
cached_prompts_path = os.path.join(os.getcwd(), config["storage"]["cached_prompts_path"] )

print(documents_path)
print(f"File exists: {os.path.exists(documents_path)}")
print(os.listdir(documents_path))
print(cached_prompts_path)
print(f"File exists: {os.path.exists(cached_prompts_path)}")

documents = read_directory(documents_path)
print(documents)