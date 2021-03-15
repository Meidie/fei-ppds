from time import sleep
from random import randint

from fei.ppds import Semaphore, Thread, Event, print
from light_switch import LightSwitch

MONITORS = 2
SENSORS = 11


class PowerPlant:
    def __init__(self):
        self.access_data = Semaphore(1)
        self.turnstile = Semaphore(1)
        self.ls_monitor = LightSwitch()
        self.ls_sensor = LightSwitch()
        self.valid_data = Event()


def monitor(power_plant: PowerPlant, monitor_id):
    power_plant.valid_data.wait()

    while True:
        sleep(0.5)
        power_plant.turnstile.wait()
        monitor_count = power_plant.ls_monitor.lock(power_plant.access_data)
        power_plant.turnstile.signal()

        print(f'Monitor {monitor_id}: '
              f'monitor count = {monitor_count}')
        power_plant.ls_monitor.unlock(power_plant.access_data)


def sensor(power_plant: PowerPlant, sensor_id):
    while True:
        power_plant.turnstile.wait()
        power_plant.turnstile.signal()

        sensor_count = power_plant.ls_sensor.lock(power_plant.access_data)
        write_time = randint(10, 15) / 1000

        print(
            f'Sensor {sensor_id}: '
            f'sensors count = {sensor_count}, '
            f'writing time {write_time} ')
        sleep(write_time)
        power_plant.valid_data.signal()
        power_plant.ls_sensor.unlock(power_plant.access_data)


def create_monitors_and_sensors(power_plant: PowerPlant, monitors: list,
                                sensors: list):
    for monitor_id in range(MONITORS):
        monitors.append(Thread(monitor, power_plant, monitor_id))

    for sensor_id in range(SENSORS):
        sensors.append(Thread(sensor, power_plant, sensor_id))


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
