import time
import msvcrt

import mqtt as MQTT
import simulator
import controller

class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

t1 = simulator.tank(80, 90, 1, 30)
sp1 = simulator.setpoint(100, 100)

tick = 0
start = time.monotonic()
MQTT.start_broker()

room_temp = 18

while True:
    old_level = t1.level
    old_temp = t1.temp

    ## таймер
    tick += 1
    dt = t1.DT
    sec = tick // t1.tickrate
    ## логика
    if msvcrt.kbhit():
        key = msvcrt.getwch()
        if key in ('a', 'A'):
            MQTT.send("cmd/ack", '1')

        if key in ('s', 'S'):
            MQTT.send("cmd/start", '1')

        if key in ('b', 'B'):
            MQTT.send("cmd/stop", '1')

    if MQTT.take_ack():
        controller.ack()

    controller.step(t1, sp1)
    t1.update(dt, room_temp)
    ## конец
    new_level = t1.level
    new_temp = t1.temp
    is_level_rising = new_level - old_level
    is_temp_rising = new_temp - old_temp
    ## таймер
    elapsed = start + tick * dt - time.monotonic()
    if elapsed > 0:
        time.sleep(elapsed)
    if tick % t1.tickrate == 0:
        MQTT.send("tank/level", new_level) ## отправляем наружу
        MQTT.send("tank/temp", new_temp)

        print(f'{sec} секунд, {new_level} мм, {new_temp} C')