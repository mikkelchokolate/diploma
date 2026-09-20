import mqtt as MQTT

from enum import Enum

class Mode(Enum):
    STOP = 0
    AUTO = 1
    ALARM = 2

current = Mode.STOP

def ack():
    global current
    if current == Mode.ALARM:
        current = Mode.STOP

def step(tank, sp):


    global current

    ## защита
    if tank.level >= tank.maxlevel - tank.overflowlevel:  ## защита
        current = Mode.ALARM


    ## обработка команд
    if MQTT.take_start() and current != Mode.ALARM:
        current = Mode.AUTO
    if MQTT.take_stop() and current != Mode.ALARM:
        current = Mode.STOP


    if current == Mode.ALARM:
        tank.pump = False
        tank.heater = False
        if tank.level > tank.maxlevel - 5:
            tank.drain = True
        else:
            tank.drain = False
    else:
        tank.drain = False

    if current == Mode.STOP:
        tank.pump = False
        tank.heater = False
        tank.drain = False


    if current == Mode.AUTO:
        # регулировка уровня
        if tank.level < sp.esteemated_level:
            tank.pump = True
        else:
            tank.pump = False

        # регулировка температуры
        if tank.temp < sp.esteemated_temp and not tank.is_empty():
            tank.heater = True
        else:
            tank.heater = False