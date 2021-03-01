# Úloha 3: Fibonacciho postupnosť
Rôzne implementácie 3. úlohy sa nachádzajú v skriptoch `fibonacci_semaphore.py`, `fibonacci_event.py`, `fibonacci_mutex.py`. Ako jednotlivé názvy naznačujú v jednom skripte je urobená implementácia pomocou semaforov v ďalšom cez eventy a v poslednom pomocou mutexu. 

Logika pri skriptoch, ktoré používajú semafor/event je taká, že pre každé vlákno vytváram vlastný semafor/event pričom všetky okrem prvého vlákna (vlákno s indexom 0) sú blokovane.
```python
class Fibonacci:
    def __init__(self, N):
        # Počet vlákien
        self.N = N
        # Pole fibonacciho postupnosti
        self.fibonacci_array = [0, 1] + [0] * self.N  # 0, 1 sú pevne dané
        # Pole semafórov pre jednotlivé vlákna
        self.semaphore_array = [Semaphore(1)] + [Semaphore(0)
                                                 for each in range(self.N)]
```
Keď prvé vlákno vypočíta svoje fibonacciho číslo dá `signal()` ďalšiemu vláknu v poradí a tento proces sa následne opakuje aj pre všetky ostatné vlákna. Keďže je potrebné aby všetky vlákna boli vytvorené ešte predtým ako sa začne počítať fibonacciho postupnosť použil som `sleep(randint(1, 10) / 10)`, nie som si však úplne istý či to takto stačí pre splnenie zadania a preto som v `fibonacci_semaphore.py` použil aj bariéru, ktorá počká na všetky vlákna a až potom sa začne výpočet.
```python
def do_fibonacci_sequence(fib, sb, thread_number):
    sb.wait()  # Bariéra
    # sleep(randint(1, 10) / 10)

    fib.semaphore_array[thread_number].wait()
    # Volanie funkcie na výpočet fibonacciho čísla
    fib.count_fibonacci_sequence(thread_number)
    fib.semaphore_array[thread_number + 1].signal()
```

Logika skriptu, ktorý využíva mutex spočíva v tom, že všetky vlákna čakajú v cykle kým na ne nepríde rad. To, ktoré vlákno je momentálne na rade sa uchováva v premennej index. Ak sa index rovná číslu vlákna, vykoná sa výpočet a index sa zvýši o jedna vďaka čomu príde na rad ďalšie vlákno.




### Otázky na zamyslenie
1. **Aký je najmenší počet synchronizačných objektov (semafory, mutexy, udalosti) potrebných na riešenie tejto úlohy?**

    Mne sa to podarilo cez jeden mutex avšak nemyslím si, že tento spôsob riešenia je úplne vhodný a najsprávnejší.


2. **Ktoré z prebratých synchronizačných vzorov sa dajú (rozumne) využiť pri riešení tejto úlohy? Konkrétne popíšte, ako sa ten-ktorý synchronizačný vzor využíva vo vašom riešení**

    Osobne som pri riešení využil synchronizačný vzor signalizácia, ostatné vzory podlá mňa nie sú vhodne pre toto zadanie vzhľadom na to, že fibonacciho postupnosť je nutné počítať serializovane (mame určenú postupnosť) a je tak potrebné vedieť vždy uvoľniť len jedno vlákno po druhom. Bariéru je možné použiť na zaručenie toho, že všetky vlákna boli vytvorené ešte pred začatím počítania.
