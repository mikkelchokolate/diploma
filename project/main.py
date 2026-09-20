import time
import msvcrt
import sys

import mqtt as MQTT
import simulator
import controller

class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

print(f'{C.BLUE}{sys.version}{C.RESET}') ## по приколу

## задаем изначальные и плановые значения
t1 = simulator.tank(80, 90, 1, 30)
sp1 = simulator.setpoint(100, 100)

## таймер
tick = 0
start = time.monotonic()
## включаем передатчик (брокер)
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
            MQTT.send("cmd/ack", 'ACK REQUESTED')

        if key in ('s', 'S'):
            MQTT.send("cmd/start", 'START REQUESTED')

        if key in ('b', 'B'):
            MQTT.send("cmd/stop", 'STOP REQUESTED')

    if MQTT.take_ack():
        controller.ack()

    controller.step(t1, sp1) ## управление
    t1.update(dt, room_temp) ## симуляция
    ## конец

    new_level = t1.level
    new_temp = t1.temp
    is_level_rising = new_level - old_level
    is_temp_rising = new_temp - old_temp

    ## каждую секунду отправляем значения level и temp, и печатаем в консоль
    if tick % t1.tickrate == 0:
        MQTT.send("tank/level", new_level) ## отправляем наружу
        MQTT.send("tank/temp", new_temp)

        if new_level > old_level:
            Lcolor = C.GREEN
        elif new_level < old_level:
            Lcolor = C.RED
        else:
            Lcolor = C.YELLOW

        if new_temp > old_temp:
            Tcolor = C.GREEN
        elif new_temp < old_temp:
            Tcolor = C.RED
        else:
            Tcolor = C.YELLOW

        print(f'{sec} секунд, {Lcolor}{new_level}{C.RESET} мм, {Tcolor}{new_temp}{C.RESET} C')

    ## таймер
    elapsed = start + tick * dt - time.monotonic()
    if elapsed > 0:
        time.sleep(elapsed)  ## дожидаемся конца тика