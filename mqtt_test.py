import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import threading

MqttBroker = "192.168.1.107"
MqttPort = 1883
SubTopic1 = "ha/tts/mqtt"
SubTopic2 = "ha/camera/mqtt"
username = 'foy'
password = 't0955787053S'
asd = "There is a person in the tensorflow"



# 設定連線成功時的Callback
def on_connect_text(client, userdata, flags, rc):
    print("Connected with result code text " + str(rc))
    client.subscribe(SubTopic1)


def on_connect_img(client_2, userdata_2, flags_2, rc_2):
    print("Connected with result code img " + str(rc_2))
    client_2.subscribe(SubTopic2)


# 設定訂閱更新時的Callback
def on_message_img(client, userdata, msg):
    f = open('1.png', 'wb+')  # 開啟檔案
    f.write(msg.payload)  # 寫入檔案
    f.close()  # 關閉檔案


# def on_message_text(client, userdata, msg):
#     content = ''
#     content = msg.payload.decode('utf-8')
#     img = plt.imread('1.png')
#     if content == "There is a person in the tensorflow":
#         return content, img





def mqtt_client_thread():
    client = mqtt.Client()
    client.on_connect = on_connect_text
    client.on_message = on_message_text
    client.username_pw_set(username, password)
    client.connect(MqttBroker, MqttPort, 60)
    client.loop_forever()


def mqtt_client_thread_2():
    client_2 = mqtt.Client()
    client_2.on_connect = on_connect_img
    client_2.on_message = on_message_img
    client_2.username_pw_set(username, password)
    client_2.connect(MqttBroker, MqttPort, 60)
    client_2.loop_forever()


if __name__ == "__main__":
    # 創建兩個執行緒分別運行 mqtt_client_thread 和 mqtt_client_thread_2 函式
    thread1 = threading.Thread(target=mqtt_client_thread)
    thread2 = threading.Thread(target=mqtt_client_thread_2)
    # 啟動執行緒
    thread1.start()
    thread2.start()

    # 等待兩個執行緒結束
    thread1.join()
    thread2.join()
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import threading

MqttBroker = "192.168.1.107"
MqttPort = 1883
SubTopic1 = "ha/tts/mqtt"
SubTopic2 = "ha/camera/mqtt"
username = 'foy'
password = 't0955787053S'
asd = "There is a person in the tensorflow"



# 設定連線成功時的Callback
def on_connect_text(client, userdata, flags, rc):
    print("Connected with result code text " + str(rc))
    client.subscribe(SubTopic1)


def on_connect_img(client_2, userdata_2, flags_2, rc_2):
    print("Connected with result code img " + str(rc_2))
    client_2.subscribe(SubTopic2)


# 設定訂閱更新時的Callback
def on_message_img(client, userdata, msg):
    f = open('1.png', 'wb+')  # 開啟檔案
    f.write(msg.payload)  # 寫入檔案
    f.close()  # 關閉檔案


# def on_message_text(client, userdata, msg):
#     content = ''
#     content = msg.payload.decode('utf-8')
#     img = plt.imread('1.png')
#     if content == "There is a person in the tensorflow":
#         return content, img





def mqtt_client_thread():
    client = mqtt.Client()
    client.on_connect = on_connect_text
    client.on_message = on_message_text
    client.username_pw_set(username, password)
    client.connect(MqttBroker, MqttPort, 60)
    client.loop_forever()


def mqtt_client_thread_2():
    client_2 = mqtt.Client()
    client_2.on_connect = on_connect_img
    client_2.on_message = on_message_img
    client_2.username_pw_set(username, password)
    client_2.connect(MqttBroker, MqttPort, 60)
    client_2.loop_forever()


if __name__ == "__main__":
    # 創建兩個執行緒分別運行 mqtt_client_thread 和 mqtt_client_thread_2 函式
    thread1 = threading.Thread(target=mqtt_client_thread)
    thread2 = threading.Thread(target=mqtt_client_thread_2)
    # 啟動執行緒
    thread1.start()
    thread2.start()

    # 等待兩個執行緒結束
    thread1.join()
    thread2.join()