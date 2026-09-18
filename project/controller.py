

def step(tank):
    if tank.alarm_flag: ## защелка alarm
        tank.pump = False
        tank.heater = False
        tank.drain = True
        return
    else:
        tank.drain = False

    if tank.level < tank.esteemated_level:
        tank.pump = True
    else:
        tank.pump = False

    if tank.temp < tank.esteemated_temp and not tank.is_empty():
        tank.heater = True
    else:
        tank.heater = False

    ## защита
    if tank.level >= tank.maxlevel - tank.overflowlevel: ## защита
        tank.pump = False
        tank.heater = False
        tank.alarm_flag = True