from flask import Flask,request,abort
from linebot import(LineBotApi,WebhookHandler,exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import  *

from line_bot_api import *
from events.basic import *
from events.oil import *

app= Flask(__name__)

@app.route("/callback",methods=["POST"])
def callback():
    signature= request.headers['X-Line-Signature']

    body=request.get_data(as_text=True)
    app.logger.info("Request body: "+body)


    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

#處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()

    ########### 使用說明 選單 油價查詢 ###########
    if message_text == "@使用說明":
        about_us_event(event)
        Usage(event)
    
    if event.message.text == "想知道油價":
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )

        # line_bot_api.reply_message(event.reply_token,buttons_template)
    

if __name__ =="__main__":
    app.run()