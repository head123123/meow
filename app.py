
from line_bot_api import *
from events.basic import *
from events.oil import *
from model.mongodb import *
from events.EXRate import *
from mqtt_test import *
from events.Msg_Template import *
import re
import twstock
import datetime
import requests
import paho.mqtt.client as mqtt
from bs4 import BeautifulSoup
from linebot.v3.messaging import MessagingApi
from linebot.models import TextSendMessage, ImageSendMessage
import time

from imgurpython import ImgurClient

client_id = 'ced93beaa3737fb'
client_secret = 'cb50c8968b3c950980d3d99a2f022f0c17001329'
client = ImgurClient(client_id, client_secret)
config = {
    'album': None,  # 如果要上傳到特定相冊，請提供相冊ID，否則保持為None
    'name': 'Image Name',
    'title': 'Image Title',
    'description': 'Image Description'
}

app = Flask(__name__)


# imgurpython

# 抓取使用者關心的股票
def cache_users_stock():
    db = constructor_stock()
    nameList = db.list_collection_names()
    users = []
    for i in range(len(nameList)):
        collect = db[nameList[i]]
        cel = list(collect.find({"tag": 'stock'}))
        users.append(cel)
    return users


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id  # 使用者id
    user_name = profile.display_name
    print(user_name)
    message_text = str(event.message.text).lower()
    msg = str(event.message.text).upper().strip()
    emsg = event.message.text
    # ######ㄏ########
    # if message_text == "user":
    #     content = profile.user_id
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(content)
    #     )
    #     print(profile.user_id)
    # #######孟和葛葛交的死邏輯要記住#######

    if message_text == '開啟監測':
        # 創建兩個執行緒分別運行 mqtt_client_thread 和 mqtt_client_thread_2 函式
        thread1 = threading.Thread(target=mqtt_client_thread)
        thread2 = threading.Thread(target=mqtt_client_thread_2)

        # 啟動執行緒
        thread1.start()
        thread2.start()
        # 回應用戶訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("已經開始監測，MQTT 連線已啟動。")
        )
        client = mqtt.Client()
        client.on_connect = on_connect_text
        client.on_message = on_message_text
        client.username_pw_set(username, password)
        client.connect(MqttBroker, MqttPort, 60)
        client.loop_forever()

        def on_connect_text(client, userdata, flags, rc):
            print("Connected with result code text " + str(rc))
            client.subscribe(SubTopic1)
        def on_message_text(client, userdata, msg):

            mqtt_text = msg.payload.decode('utf-8')
            img = plt.imread('1.png')
            if mqtt_text == asd:
                mqtt_state = (mqtt_text == asd)
                print(str(mqtt_text == asd) + " mqtt_test")
                mqtt_text_content = mqtt_text
                mqtt_img_content = img
                mqtt_text = ''
                return mqtt_state,mqtt_text_content,mqtt_img_content

        while True:
            mqtt_state, mqtt_text_content, mqtt_img_content = on_message_text(client, userdata, msg)
            print(mqtt_state, mqtt_text_content,mqtt_img_content)
            print(str(mqtt_state) + "app")

            if mqtt_state:
                line_bot_api.push_message(
                    uid,
                    TextSendMessage(mqtt_text_content)
                )
                local_img_file = "1.png"
                print("Uploading image... ")
                image = client.upload_from_path(local_img_file, config=config, anon=False)
                print("Done")
                print(image)

                imgur = str(image['link'])
                print(imgur)
                line_bot_api.push_message(
                    uid, ImageSendMessage(
                        original_content_url=imgur,
                        preview_image_url=imgur
                    ))
                del mqtt_state
                thread1.join()
                thread2.join()

            # elif message_text == '關閉監測':
            #     exit()

        # 假設 on_message_text 能夠回傳 content 和 img

if __name__ == "__main__":
    app.run()

