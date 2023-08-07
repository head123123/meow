from flask import Flask,request,abort
from linebot import(LineBotApi,WebhookHandler,exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import  *

line_bot_api= LineBotApi("jypHYTQnlqOxsCS5uAFLEZinzlIt8StLZQPZEwt4gGOAg3fMHsJ4s2w8cjsOyiJyIv4rcrn6j/lxSunTeidVW86/GYsgw/aYl7xCPSsiVbSf8uSMr1wF/9KzwgUjBOK1M6gjmP/b/4jrohT7wbi8KwdB04t89/1O/w1cDnyilFU=")
handler=WebhookHandler("21e01a4b51f588aef40ca3b72d174f73")
