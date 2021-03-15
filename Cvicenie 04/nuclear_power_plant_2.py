from time import sleep
from random import randint
from typing import Callable
from fei.ppds import Semaphore, Thread
from light_switch import LightSwitch

MONITORS = 8
P_SENSORS = 1
T_SENSORS = 1
H_SENSORS = 1


class PowerPlant:
    def __init__(self):
        self.access_data = Semaphore(1)
        self.ls_monitor = LightSwitch()
        self.ls_sensor = LightSwitch()


def monitor(power_plant: PowerPlant, monitor_id):
    pass


def sensor(power_plant: PowerPlant, sensor_id, time: Callable[[], float]):
    pass


def create_monitors_and_sensors(power_plant: PowerPlant, monitors: list,
                                sensors: list):
    # Monitors
    for monitor_id in range(MONITORS):
        monitors.append(Thread(monitor, power_plant, monitor_id))

    # P, T sensors
    for sensor_id in range(P_SENSORS + T_SENSORS):
        sensors.append(Thread(sensor, power_plant, sensor_id,
                              lambda: randint(10, 20) / 1000))
    # H sensors
    for sensor_id in range(H_SENSORS):
        sensors.append(Thread(sensor, power_plant, len(sensors) + sensor_id,
                              lambda: randint(20, 25) / 1000))


def wait_to_finish(monitors: list, sensors: list):
    for m in monitors:
        m.join()

    for s in sensors:
        s.join()


def main():
    power_plant = PowerPlant()
    monitors, sensors = list(), list()

    create_monitors_and_sensors(power_plant, monitors, sensors)
    wait_to_finish(monitors, sensors)


if __name__ == '__main__':
    main()
