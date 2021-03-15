from time import sleep
from random import randint
from typing import Callable
from fei.ppds import Semaphore, Thread, Event, print
from light_switch import LightSwitch

MONITORS = 8
P_SENSORS = 1
T_SENSORS = 1
H_SENSORS = 1


class PowerPlant:
    def __init__(self):
        self.access_data = Semaphore(1)
        self.turnstile = Semaphore(1)
        self.ls_monitor = LightSwitch()
        self.ls_sensor = LightSwitch()
        self.sensors_updated = Event()


def monitor(power_plant: PowerPlant, monitor_id):
    # počkanie na aktualizáciu všetkých čidiel
    power_plant.sensors_updated.wait()

    while True:
        # monitory prechadzajú cez turniket, pokým ho nezamkne senzor
        power_plant.turnstile.wait()
        power_plant.turnstile.signal()

        # získanie prístupu k úložisku
        operator_count = power_plant.ls_monitor.lock(power_plant.access_data)

        # čítanie/aktualizácia dát
        read_time = randint(40, 50) / 1000
        print(
            f'Monitor {monitor_id}: '
            f'number of reading monitors = {operator_count}, '
            f'reading time = {read_time:.3f}s')
        sleep(read_time)

        # odchod z úložiska
        power_plant.ls_monitor.unlock(power_plant.access_data)


def sensor(power_plant: PowerPlant, sensor_id, time: Callable[[], float]):
    while True:
        # zablokovanie turniketu
        power_plant.turnstile.wait()
        # získanie prístupu k úložisku
        sensor_count = power_plant.ls_sensor.lock(power_plant.access_data)
        power_plant.turnstile.signal()

        # zápis/aktualizácia dát
        write_time = time()
        print(
            f'Sensor {sensor_id}: '
            f'number of writing sensors = {sensor_count}, '
            f'writing time = {write_time:.3f}s')
        sleep(write_time)

        # odchod z úložiska
        power_plant.ls_sensor.unlock(power_plant.access_data)
        # signalizácia, že všetky čidlá vykonali aktualizáciu
        power_plant.sensors_updated.set()

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
