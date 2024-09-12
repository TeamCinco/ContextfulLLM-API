from document_qna.setup import get_qna
from document_qna.qna import QnA

qna_instance = get_qna()

while True:
    user_msg = input("Input current user message (type \"quit\" to exit): ")
    if user_msg == "quit":
        break
    bot_msg = qna_instance(user_msg)
    print(bot_msg)