# External imports:
import configparser
import os
from dotenv import load_dotenv
from openai import OpenAI
from functools import partial

# Internal imports
from .qna import QnA
from .file_loader import read_directory
from .hash_directory import hash_directory
from .llm_prompt import llm_prompt, default_msg
from .get_response import get_response

# importing variables from config
config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), 'settings.ini')
config.read(config_path)

# Loading .env file
dotenv_path = os.path.join(os.getcwd(), '..', '.env')
load_dotenv(dotenv_path)

# Storage
# documents_path = os.path.join(os.getcwd(), '..', config["storage"]["documents_path"] )
documents_path = os.path.join(os.getcwd(), config["storage"]["documents_path"] )
cached_prompts_path = os.path.join(os.getcwd(), config["storage"]["cached_prompts_path"] )

# Inference
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
model = str(config["inference"]["model"])
temperature = float(config["inference"]["temperature"])

client_args = {
"model": model,
"temperature": temperature, # To tune
}

# Other settings
verbosity: bool = config["other_settings"]["verbosity"]
cache_prompts: bool = config["other_settings"]["cache_prompts"]


# Main setup/ helper process
def get_qna() -> QnA: 
    print("starting getqna process")
    documents = read_directory(documents_path)
    prompt = llm_prompt + str(documents)
    default_message = default_msg
    response_func = get_inference_func()
    
    qna_instance = QnA(prompt=prompt, default_msg=default_message, response_func=response_func)
    return qna_instance

    

# # Creating the prompt
# # Hash entire "Documents" folder to see if there is a cached version
# def get_sys_prompt():
    
#     # Make prompt every time if no cache
#     if not cache_prompts:  
#         prompt = make_sys_prompt()
#         return prompt
        
#     directory_hash = hash_directory(documents_path)
#     prompt_cached = check_prompt_cached(directory_hash)
    
#     prompt_file_path = os.path.join(cached_prompts_path, str(directory_hash) + ".txt")
#     if prompt_cached:
#         with open(prompt_file_path, 'r') as file:
#             prompt = file.read()
#     else:
#         prompt = make_sys_prompt()
#         with open(prompt_file_path, "w") as file:
#             file.write(prompt)    
#     return prompt


# def check_prompt_cached(directory_hash):
#     prompt_file_name = str(directory_hash) + ".txt"  
#     prompt_file_path = os.path.join(cached_prompts_path, prompt_file_name)
#     if os.path.isfile(prompt_file_path):
#         return True
#     return False


# def make_sys_prompt():
#     documents = read_directory(documents_path)
#     print("Printing Documents")
#     print(documents)
#     prompt = llm_prompt + str(documents)
#     print("Printing Final Prompt")
#     print(prompt)
#     return prompt

# See https://openrouter.ai/docs/parameters
def get_inference_func():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key = OPENROUTER_API_KEY,
    )
    response_func = partial(get_response, client = client, client_args = client_args)
    return response_func