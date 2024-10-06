import configparser
import os
from typing import Callable, List, Union
from dotenv import load_dotenv
from openai import OpenAI
from functools import partial

# Internal imports
from ..qna import QnA
from .file_loader import read_directory
from .llm_prompt import llm_prompt, llm_prompt_finance, default_msg
from .get_response import get_response
from .get_finance import fetch_stock_data

# Configuration setup
def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config_path = os.path.join(os.getcwd(), 'settings.ini')
    config.read(config_path)
    return config

# Load configuration and environment variables
config = load_config()
dotenv_path = os.path.join(os.getcwd(), '..', '.env')
load_dotenv(dotenv_path)

# Storage paths
documents_path = os.path.join(os.getcwd(), config["storage"]["documents_path"])
cached_prompts_path = os.path.join(os.getcwd(), config["storage"]["cached_prompts_path"])

# Inference settings
CLIENT_API_KEY = os.getenv("CLIENT_API_KEY")
base_url = str(config["inference provider"]["base_url"])

# Create a dictionary from the inference arguments section
inference_args = {key: value for key, value in config["infernce arguments"].items()}

# Convert types for specific keys
# TODO: pack everything in a function and add type conversion for all commonly used arguments
if "max_tokens" in inference_args:
    inference_args["max_tokens"] = int(inference_args["max_tokens"])
if "temperature" in inference_args:
    inference_args["temperature"] = float(inference_args["temperature"])
if "model" in inference_args:
    inference_args["model"] = str(inference_args["model"])

# Other settings
verbosity: bool = config["other_settings"]["verbosity"]
cache_prompts: bool = config["other_settings"]["cache_prompts"]

def get_inference_func() -> Callable:
    client = OpenAI(base_url=base_url, api_key=CLIENT_API_KEY)
    return partial(get_response, client=client, client_args=inference_args)

def get_qna() -> QnA:
    documents = read_directory(documents_path)
    prompt = llm_prompt + str(documents)
    response_func = get_inference_func()
    
    return QnA(prompt=prompt, default_msg=default_msg, response_func=response_func)

def get_qna_finance(tickers: Union[List[str], str], *args, **kwargs) -> QnA:
    tickers = tickers if isinstance(tickers, list) else [tickers]
    documents = fetch_stock_data
    prompt = llm_prompt_finance + str(documents)
    response_func = get_inference_func()
    
    return QnA(prompt=prompt, default_msg=default_msg, response_func=response_func)

