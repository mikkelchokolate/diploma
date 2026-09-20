import paho.mqtt.client as mqtt

MQTT_OK = False

last_values = {
    "connection": 0,
    "level": -1,
    "temperature": -1
}

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        mqtt_client.subscribe("#")
        global MQTT_OK
        MQTT_OK = True
        print("Connected to MQTT Broker")
    else:
        print("Could not connect to MQTT Broker")

def on_disconnect(client, userdata, flags, rc, properties):
    global MQTT_OK
    MQTT_OK = False
    print("Disconnected from MQTT Broker")

def on_message(client, userdata, msg):
    if msg.topic == "conn/ok":
        last_values["connection"] = msg.payload
    elif msg.topic == "tank/level":
        last_values["level"] = msg.payload
    elif msg.topic == "tank/temp":
        last_values["temperature"] = msg.payload

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message

def start():
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()

def stop():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()