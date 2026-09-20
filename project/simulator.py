## Simulator

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