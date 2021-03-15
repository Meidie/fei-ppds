from time import sleep
from random import randint
from typing import Callable
from fei.ppds import Semaphore, Thread, Event, print
from light_switch import LightSwitch
from barrier import Barrier

MONITORS = 8
P_SENSORS = 1
T_SENSORS = 1
H_SENSORS = 1


class PowerPlant:
    def __init__(self):
        self.barrier = Barrier(P_SENSORS + T_SENSORS + H_SENSORS)
        self.access_data = Semaphore(1)
        self.ls_monitor = LightSwitch()
        self.ls_sensor = LightSwitch()
        self.sensors_ready = Event()


def monitor(power_plant: PowerPlant, monitor_id):
    while True:
        # počkanie na všetky čidlá
        power_plant.sensors_ready.wait()
        # získanie prístupu k úložisku
        operator_count = power_plant.ls_monitor.lock(power_plant.access_data)

        # čítanie/aktualizácia dát
        read_time = randint(40, 50) / 1000
        print(
            f'Monitor {monitor_id}: '
            f'number of reading monitors = {operator_count}, '
            f'reading time = {read_time}s')
        sleep(read_time)

        # reset eventu
        power_plant.sensors_ready.clear()

        # odchod z úložiska
        power_plant.ls_monitor.unlock(power_plant.access_data)


def sensor(power_plant: PowerPlant, sensor_id, time: Callable[[], float]):
    while True:
        # získanie prístupu k úložisku
        sensor_count = power_plant.ls_sensor.lock(power_plant.access_data)

        # zápis/aktualizácia dát
        write_time = time()
        print(
            f'Sensor {sensor_id}: '
            f'number of writing sensors = {sensor_count}, '
            f'writing time = {write_time}s')
        sleep(write_time)

        # počkanie na aktualizáciu všetkých čidiel
        power_plant.barrier.wait()
        # odchod z úložiska
        power_plant.ls_sensor.unlock(power_plant.access_data)
        # signalizácia, že všetky čidlá vykonali aktualizáciu
        power_plant.sensors_ready.set()

        # prestávka aktualizácie čidiel
        sleep(randint(50, 60) / 1000)


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
