import paho.mqtt.client as mqtt
subscribe = "massukan_kata"
def on_message(client, userdata, msg):
    data= str(msg.payload.decode())
    print(data)
    return
client = mqtt.Client()
client.on_message = on_message
server = "broker.hivemq.com"
client.connect(server, 1883)
client.subscribe(subscribe)

print("menunggu pesan")
client.loop_forever()