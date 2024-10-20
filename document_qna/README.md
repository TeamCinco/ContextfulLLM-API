
# Creating a QnA instance

The `QnA` class is the main entry point of this repository, below are some ways you can initialize it.

Perform chat according to provided questions

```python
# from main.py, example usage
from document_qna.setup import get_qna
from document_qna.qna import QnA

qna_instance: QnA = get_qna() # loads documents from specified folder directly, see settings.ini

while True:
    user_msg = input("Input current user message (type \"quit\" to exit): ")
    if user_msg == "quit":
        break
    bot_msg = qna_instance(user_msg)
    print(bot_msg)
```

Performing chating according to financial data (data pulled from `yfinance`)

```python
# from main_finance.py, example usage
from document_qna.setup import get_qna_finance
from document_qna.qna import QnA


tickers = ["TSLA", "APPL"]
period = "1mo"

qna_instance: QnA = get_qna_finance(tickers, period)

# Rest same as main.py
```

Or, you may initialize the `QnA` instance by providing your own system prompt (including the documents), default assistant message (can be None) and an inference callable, which takes in a message and returns a system/llm response

```python
# from document_qna/setup.py
documents = read_directory(documents_path)
prompt = llm_prompt + str(documents)
default_message = default_msg
response_func = get_inference_func()

qna_instance = QnA(prompt=prompt, default_msg=default_message, response_func=response_func)
```
