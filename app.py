from flask import Flask,request,abort
from linebot import(LineBotApi,WebhookHandler,exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import  *


app= Flask(__name__)




line_bot_api= LineBotApi("jypHYTQnlqOxsCS5uAFLEZinzlIt8StLZQPZEwt4gGOAg3fMHsJ4s2w8cjsOyiJyIv4rcrn6j/lxSunTeidVW86/GYsgw/aYl7xCPSsiVbSf8uSMr1wF/9KzwgUjBOK1M6gjmP/b/4jrohT7wbi8KwdB04t89/1O/w1cDnyilFU=")
handler=WebhookHandler("21e01a4b51f588aef40ca3b72d174f73")

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message=TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token , message)


if __name__ =="__main__":
    app.run()