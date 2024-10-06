## How to use:

Obtain a `QnA` instance via one of the helper functions from `get_qna` and provide the instance with the user query, a system/ bot response will be returned and the instance will automatically store the chat history:

```python
# from main.py, example usage
from document_qna.setup import get_qna
from document_qna.qna import QnA

qna_instance: QnA = get_qna()

while True:
    user_msg = input("Input current user message (type \"quit\" to exit): ")
    if user_msg == "quit":
        break
    bot_msg = qna_instance(user_msg)
    print(bot_msg)
```

or

```python
# from main_finance.py, example usage
from document_qna.setup import get_qna_finance
from document_qna.qna import QnA


tickers = ["TSLA", "APPL"]
period = "1mo"

qna_instance: QnA = get_qna_finance(tickers, period)

# Rest same as main.py
```


or, you may initialize the `QnA` instance by providing your own system prompt (including the documents), default assistant message (can be None) and an inference callable, which takes in a message and returns a system/llm response

```python
# from document_qna/setup.py
documents = read_directory(documents_path)
prompt = llm_prompt + str(documents)
default_message = default_msg
response_func = get_inference_func()

qna_instance = QnA(prompt=prompt, default_msg=default_message, response_func=response_func)
```

## Setup

1. Place instruction documents in the documents folder
2. Provide your openrouter api key in a .env folder
3. Change nessesary settings in settings.ini (affects behavior of the `get_qna()` setup function only).
