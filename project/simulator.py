import sys
import time


class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

print(f'{C.BLUE}{sys.version}{C.RESET}')
# print(f'{C.BLUE}Simulator{C.RESET}')
# print()


# class node:
#     def __init__(self,x,y):
#         self.x = x
#         self.y = y

class setpoint:
    def __init__(self, esteemated_level=-1, esteemated_temp=-1):
        self.esteemated_level = esteemated_level
        self.esteemated_temp = esteemated_temp


class tank:
    pump: bool
    heater: bool
    drain: bool

    tickrate = 60
    DT = 1 / tickrate

    heat_speed = 0.8
    cold_speed = 0.01
    drain_speed = 0.7
    pumping_speed = 0.8

    def __init__(self, level=-1, maxlevel = -1, overflowlevel = -1, temp=-1):
        # включение
        self.pump = False
        self.heater = False
        self.drain = False

        self.level = level                       # мм
        self.maxlevel = maxlevel                 # мм
        self.overflowlevel = overflowlevel
        self.temp = temp                         # градусы C



    def is_valid(self):
        return self.level >= 0 and self.temp >= 0

    def is_empty(self):
        return self.level <= 0

    def heat(self, degrees):
        self.temp += degrees

    def update(self, dt, room_temp):
        if not self.is_valid():
            return

        _heat_speed = self.heat_speed
        _cold_speed = self.cold_speed
        _drain_speed = self.drain_speed
        _pumping_speed = self.pumping_speed

        if not self.pump:
            _pumping_speed = 0
        else:
            _pumping_speed = self.pumping_speed

        if not self.heater:
            _heat_speed = 0
        else:
            _heat_speed = self.heat_speed

        if not self.drain:
            _drain_speed = 0
        else:
            _drain_speed = self.drain_speed

        _dt = dt
        _room_temp = room_temp

        ## пред логика
        if self.temp >= 100:
            self.temp = 100

        if self.level <= 0:
            heat_through_tick = 0.002
            self.level = 0

        if self.level >= self.maxlevel:
            self.level = self.maxlevel
        ### логика
        self.level += _pumping_speed * _dt
        self.level -= _drain_speed * _dt
        self.temp += _heat_speed * _dt
        self.temp -= _cold_speed * (self.temp - _room_temp) * _dt
        ### пост логика
        if self.level <= 0:
            self.level = 0

        if self.level >= self.maxlevel:
            self.level = self.maxlevel

        if self.temp >= 100:
            self.temp = 100
        ## конец пост логика


# t1 = tank(8, 20,30)

# print(f'is valid? {t1.is_valid()}')
# print(f'is empty? {t1.is_empty()}')
# print(f'{t1.temp} градусов')
# print(f'{t1.level} мм')
# print(f'{t1.temp} градусов')


# tick = 0
# start = time.monotonic()

#пред логика
# t1.pump = True
# while(True):
#     tick += 1
#     sec = tick//t1.tickrate
#     target = start + tick * t1.DT
    ## alarm catch
    # t1.alert() ## не его собачье дело

    #логика управления
    # if sec == 6:
    #     t1.pump = False
    #     t1.heater = True
    #
    # if sec == 10:
    #     t1.heater = False
    #     t1.drain = True
    ## логика
    # t1.update(t1.DT, 18)
    ## отсчитываем каждый тик 60 тиков в секунду
    # now = time.monotonic()
    # if target > now:
    #     time.sleep(target-now)
    # if tick % 60 == 0:
    #     print(f'{sec} секунд, {t1.level} мм, {t1.temp} градусов')