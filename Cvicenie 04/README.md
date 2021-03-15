# Cvičenie 4: Atomová elektráreň #2

### Analýza
Ide o úlohu vzájomného vylúčenia kategórií procesov. Monitory tvoria jednu kategóriu a čidlá tvoria druhú kategóriu. Pre obe kategórie platí, že viacerí členovia kategórie môžu naraz pristupovať k údajom, a to z toho dôvodu, že monitory údaje len čítajú a čidlá údaje zapisujú do svojich osobitných priestorov. Každý monitor sa neustále pokúša aktualizovať údaje pričom samotná aktualizácia trvá 40-50 ms. Na druhú stranu čidlá sa snažia aktualizovať údaje každých 50-60 ms pričom samotná aktualizácia trvá buď 10-20 ms alebo 20 - 25 ms v závislosti od typu čidla. Monitory môžu začať pracovať iba vtedy, keď už všetky čidlá dodali do úložiska platné údaje. 

Na zaručenie toho aby monitory mohli začať aktualizáciu až potom ako všetkých čidlá vykonali svoju aktualizáciu využijeme event (udalosť). Monitory sú blokované eventom. Event je nastavený až potom ako všetky čidlá prvykrát vykonajú aktualizáciu. Kedže monitory môžu neustále aktualizovať svoje hodnoty treba zaručiť aby nenastalo vyhladovenie senzorov. To vyriešime zavedením turniketu (dĺžka aktualizácie monitorov a senzorov je pre toto použitie v poriadku). Vzájomné vylúčenie kategórií je implementované pomocou vypínačov.

### Pseudokód
```
def init():
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = LightSwitch()
    ls_sensor = LightSwitch()
    sensors_updated = Event()
 
    for monitor_id in <0,7>:
        create_and_run_thread(monitor, monitor_id)
    for sensor_id in <0,2>:
        create_and_run_thread(sensor, sensor_id, rand(10 az 20 ms))
    for sensor_id in <0,1>:
        create_and_run_thread(sensor, sensor_id, rand(20 az 25 ms))


def monitor(monitor_id):

    // monitory čakajú kým všetky čidlá aktualizujú svoju hodnotu
    sensors_updated.wait()

    while True:
        // monitory prechadzajú cez turniket, pokým ho nezamkne senzor
        turnstile.wait()
        turnstile.signal()      

        // získanie prístupu k úložisku
        monitor_count = ls_monitor(access_data).lock()
        
        // čítanie dát
        read_time = rand(40 az 50 ms)
        print('monit "%02d": monitor_count=%02d, read_time=%03d\n')
        // trvanie čítania
        sleep(read_time)
       
        // odchod z úložiska
        ls_monitor(access_data).unlock()


def sensor(sensor_id, update_time):
    while True:
        // zablokovanie turniketu, aby senzory mohli ziskat pristup
        turnstile.wait()
        // získanie prístupu k úložisku
        sensor_count = ls_sensor(access_data).lock()
        turnstile.signal()
        
        // zápis dát
        write_time = update_time
        print('cidlo "%02d": sensor_count=%02d, write_time=%03d\n')
        // trvanie zápisu
        sleep(write_time)
        
        // odchod z úložiska
        ls_sensor.unlock(access_data)
        // signalizácia, že všetky čidlá vykonali aktualizáciu
        sensors_ready.set()
        
        // prestávka čidiel 
        sleep(rand(50 az 60 ms))
```
### Záver
Ak na riešenie tejto úlohy použijeme vzájomné vylúčenie kategórií s turniketom, ktorý zamyká senzory, tak vieme túto úlohu jednoducho a efektívne vyriešiť.