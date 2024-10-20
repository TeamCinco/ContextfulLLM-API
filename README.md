# FAQ-LLM-BOT (abstracted inferface)

## How to use

Obtain a `QnA` instance via one of the helper functions from `get_qna` and provide the instance with the user query, a system/ bot response will be returned and the instance will automatically store the chat history:

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

Check other ways of initializing a QnA object [here](document_qna/README.md)

## Restarting chat from index

To restart the chat from a certain index (w.r.t. only the chat history), you can do the following:

```python
qna_instance.restart_from_index(<index number>)
```

Say, you have the following chat history:

```python
[
    {"role": "system", "content": "Some system prompt"}, # Is not counted
    {"role": "assistant", "content": "Default message e.g. how can I help you today"}, # Is not counted
    {"role": "user", "content": "blah blah blah"}, # index = 1
    {"role": "assistant", "content": "blah blah blah blah"}, # index = 2
    {"role": "user", "content": "yada yada yada"}, # index = 3
    {"role": "assistant", "content": "yada yada yada yada"}, # index = 4
]
```

And then you do

```python
qna_instance.restart_from_index(2)
```

Then the new chat history becomes:

```python
[
    {"role": "system", "content": "Some system prompt"}, # Is not counted
    {"role": "assistant", "content": "Default message e.g. how can I help you today"}, # Is not counted
    {"role": "user", "content": "blah blah blah"}, # index = 1
    {"role": "assistant", "content": "blah blah blah blah"}, # index = 2
]
```

## Storing chat and reviving it later

A user might want to perform a chat across multiple sessions, where we won't keep the session alive.

We can store all relevant information of the instance using:

```python
prompt, default_msg, chat_history = qna_instance.save_chat()

# Store `prompt, default_msg, chat_history` somewhere 
some_storage_function(prompt, default_msg, chat_history)
```

Then, we can retrieve the chat using:

```python
prompt, default_msg, chat_history = some_retrieval_function()
response_func = get_inference_func() # example function, check document_qna/setup/setup.py

qna_instance = QnA(prompt=prompt, default_msg=default_message, response_func=response_func, chat_history = chat_history)

# Use this qna_instance for chatting
```

## Setup

1. Place instruction documents in the documents folder
2. Provide the api key of a provider of your choice in a .env folder (check (and clone) the [.env.template](.env.template) file)
3. Change nessesary settings in settings.ini (affects behavior of the `get_qna()` setup function only).
