import paho.mqtt.client as client
import time

cli = client.Client()

cli.connect("192.168.2.11",1883)

cli.publish("test","hello from python")
cli.subscribe("#")

def fctReceptionMsg(ud,c, m):
    print(f"{m.topic}:{m.payload}")

def fctTopicTemperature(ud,c,m):
    print(f"Temperature: {m.payload}")

def fctTopicImage(ud,c,m):
    print("Image reçue")

cli.message_callback_add("Image",fctTopicImage)
cli.message_callback_add("Temperature",fctTopicTemperature)

cli.on_message = fctReceptionMsg

cli.loop_start()

while True:
    print("Je suis dans ma boucle")
    time.sleep(5)

cli.loop_stop()
 