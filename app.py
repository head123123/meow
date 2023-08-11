from line_bot_api import *
from events.basic import *
from events.oil import *
from events.Msg_Template import *
from events.EXRate import *
import re
import twstock
import datetime

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
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id
    message_text = str(event.message.text).lower()
    msg = str(event.message.text).upper().strip()
    emsg = event.message.text #同message_text
    user_name=profile.display_name #使用者名稱

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

    # ############"股價查詢"############
    if message_text == "股價查詢":
        line_bot_api.push_message(
        uid, 
        TextSendMessage("請輸入'#' + '股票代號'\n範例：#2330")
        )

    #股價查詢
    if re.match("想知道股價[0-9]" , msg):
        stockNumber = msg[5:9]
        btn_msg = stock_reply_other(stockNumber)
        line_bot_api.push_message(uid , btn_msg)
        return 0
    
    if (emsg.startswith('#')):
        text = emsg[1:]
        content =''

        stock_rt = twstock.realtime.get(text)
        my_datetime = datetime.datetime.fromtimestamp(stock_rt['timestamp']+8*60*60)
        my_time = my_datetime.strftime('%H:%M:%S')

        content +='%s (%s) %s\n' % (
            stock_rt['info']['name'],
            stock_rt['info']['code'],
            my_time)
        
        content += '現價: %s / 開盤: %s\n'%(
            stock_rt['realtime']['latest_trade_price'],
            stock_rt['realtime']['open'])
        
        content += '最高: %s / 最低:%s\n'%(
            stock_rt['realtime']['high'],
            stock_rt['realtime']['low'])
        
        content += '量: %s\n'%(stock_rt['realtime']['accumulate_trade_volume'])

        stock = twstock.Stock(text)
        content += '-----\n'
        content += '最近五日價格: \n'
        price5 = stock.price[-5:][::-1]
        date5 = stock.date[-5:][::-1]
        for i in range(len(price5)):
            content += '[%s] %s\n' % (date5[i].strftime("%Y-%m-%d"), price5[i])
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=content)
        )

    #############匯率區###############
    if re.match("幣別種類",emsg):
        message = show_Button()
        line_bot_api.reply_message(event.reply_token,message)
    if re.match("換匯[A-Z]{3}",msg):
        msg = msg[4:]
        content = showCurrency(msg)
        line_bot_api.push_message(uid,TextSendMessage(content))
    if re.match("換匯[A-Z]{3}/[A-Z]{3}/[0-9]", msg):
        line_bot_api.push_message(uid, TextSendMessage("正在為您計算..."))
        content = getExchangeRate(msg)
        line_bot_api.push_message(uid, TextSendMessage(content))
     # ############"@小幫手"############
    if message_text == "@小幫手":
        button_template = ButtonsTemplate()
        line_bot_api.reply_message(
        event.reply_token, button_template
        )

        


@handler.add(FollowEvent)
def handle_follow(event):
    emojis = [
        {
            "index": 0, 
            "productId": "5ac21a18040ab15980c9b43e", 
            "emojiId": "009"
        }, 
        {
            "index": 16, 
            "productId": "5ac21a18040ab15980c9b43e", 
            "emojiId": "014"
        }
    ]

    welcome_message = TextSendMessage(text='''$ Agave Finance $
    您好，歡迎加入成為 Agave Finance 的好友!!!
    我是Agave財經小幫手~
    下方選單有：
    股票查詢、油價查詢、匯率查詢、自動提醒、資訊整理、使用說明
    使用上有任何問題可以參考使用說明''', emojis=emojis)

    line_bot_api.reply_message(
        event.reply_token, welcome_message
        )
    

@handler.add(UnfollowEvent)
def hadle_unfollow(event):
    print(event)


if __name__ == "__main__":
    app.run()
