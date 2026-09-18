import time
import msvcrt

import simulator
import controller

class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

t1 = simulator.tank(80,90, 1, 100, 30, 100)

tick = 0
start = time.monotonic()

while(True):
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
            t1.ack()

    controller.step(t1)
    t1.update(dt, 18)
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
        match t1.alarm_flag:
            case True:
                print(f'{C.RED}{sec} секунд, {t1.level} мм, {t1.temp} C{C.RESET}')
            case _:
                if is_level_rising > 0:
                    if is_temp_rising > 0:
                        print(f'{sec} секунд, {C.GREEN}{t1.level}{C.RESET} мм, {C.GREEN}{t1.temp}{C.RESET} C')
                    elif is_temp_rising < 0:
                        print(f'{sec} секунд, {C.GREEN}{t1.level}{C.RESET} мм, {C.RED}{t1.temp}{C.RESET} C')
                    else:
                        print(f'{sec} секунд, {C.GREEN}{t1.level}{C.RESET} мм, {t1.temp} C')
                elif is_level_rising < 0:
                    if is_temp_rising > 0:
                        print(f'{sec} секунд, {C.RED}{t1.level}{C.RESET} мм, {C.GREEN}{t1.temp}{C.RESET} C')
                    elif is_temp_rising < 0:
                        print(f'{sec} секунд, {C.RED}{t1.level}{C.RESET} мм, {C.RED}{t1.temp}{C.RESET} C')
                    else:
                        print(f'{sec} секунд, {C.RED}{t1.level}{C.RESET} мм, {t1.temp} C')
                elif is_temp_rising > 0:
                    print(f'{sec} секунд, {t1.level} мм, {C.GREEN}{t1.temp}{C.RESET} C')
                elif is_temp_rising < 0:
                    print(f'{sec} секунд, {t1.level} мм, {C.RED}{t1.temp}{C.RESET} C')
                else:
                    print(f'{sec} секунд, {t1.level} мм, {t1.temp} C')