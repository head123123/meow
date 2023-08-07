from line_bot_api import *

def about_us_event(event):
    # message=TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token , message)
    emoji = [
            {
                "index":0,
                "productId":"5ac1bfd5040ab15980c9b435",
                "emojiId":"009"
            },
            {
                "index":17,
                "productId":"5ac21e6c040ab15980c9b444",
                "emojiId":"002"
            }
    ]

    text_message = TextSendMessage(text='''$ Master Finance $
Hello! 您好，歡迎您成為 Master Finance 的好友！
                                   
我是Master 財經小幫手
                                   
-這裡有股票、匯率資訊哦～
-直接點選下方[圖中]選單功能
                                   
期待您的光臨''',emojis=emoji)
    sticker_message = StickerMessage(
        package_id='8522',
        sticker_id='16581271'
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message,sticker_message])
    
def push_msg(event,msg):
    try:
        user_id = event.source.user_id
        line_bot_api.push_message(user_id,TextSendMessage(text=msg))
    except:
        room_id = event.source.room_id
        line_bot_api.push_message(room_id,TextSendMessage(text=msg))

def Usage(event):
    push_msg(event,"    😼😼查詢方法😼😼    \
             \n\
             \n👍小幫手可以查詢油價、匯率、股價👍\
             \n\
             \n❤️油價通知➡➡➡輸入查詢油價❤️\
             \n🧡匯率通知➡➡➡輸入查詢匯率🧡\
             \n💛匯率兌換➡➡➡換匯USD/TWD💛\
             \n💜股價查詢➡➡➡輸入#股票代號💜")


