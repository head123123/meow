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