import paho.mqtt.client as mqtt

ack_requested = False
start_requested = False
stop_requested = False

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        mqttc.subscribe("cmd/#")
        print("Connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.topic == "cmd/ack":
        global ack_requested
        ack_requested = True

    if msg.topic == "cmd/start":
        global start_requested
        start_requested = True

    if msg.topic == "cmd/stop":
        global stop_requested
        stop_requested = True

def send(topic, attr):
    mqttc.publish(topic, attr)
    # print(f'sent {attr}')

def take_ack():
    global ack_requested
    temp = ack_requested
    ack_requested = False
    return temp

def take_start():
    global start_requested
    temp = start_requested
    start_requested = False
    return temp

def take_stop():
    global stop_requested
    temp = stop_requested
    stop_requested = False
    return temp

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

def start_broker():
    mqttc.connect("localhost", 1883, 60)
    mqttc.loop_start()

def stop_broker():
    mqttc.loop_stop()
    mqttc.disconnect()