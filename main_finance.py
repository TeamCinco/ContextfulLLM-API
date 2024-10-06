from document_qna.setup.setup import get_qna_finance
from document_qna.qna import QnA

tickers = ["TSLA", "APPL"]
period = "1mo"

qna_instance: QnA = get_qna_finance(tickers, period)

while True:
    user_msg = input("Input current user message (type \"quit\" to exit): ")
    if user_msg == "quit":
        break
    bot_msg = qna_instance(user_msg)
    print(bot_msg)