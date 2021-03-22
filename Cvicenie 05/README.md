# Cvičenie 5: Problém divochov #2

### Analýza
Jedná sa o úlohu, pri ktorej sa využíva synchronizačný vzor signalizácia. Jeden divoch vždy signalizuje kuchárovi, že je hrniec prázdny a treba začať variť a na druhej strane kuchár signalizuje divochom, že hrniec bol naplnený a môžu začať hodovať. Problém je založený na princípe producentov (kuchár) a konzumentov (divosi), pričom máme, ale obmedzenia, že producent (kuchár) pridáva porcie len keď už je hrniec prázdny, konzumenti (divosi) zatiaľ čakajú. Po naplnení hrnca divosi hodujú a kuchár čaká kým nebude hrniec opäť prázdny. Vzhľadom na to, že k hrncu môže mať vždy prístup len jedna kategória je potrebné použiť aj vzor vzájomného vylúčenia kategórii.

Oproti štandardnému problému hodujúcich divochov má náš kmeň viacero kuchárov. Kuchári začínajú variť spolu naraz, pričom si medzi sebou rozdelia prácu rovnomerne. Po skončení varenia sa všetci počkajú na bariére aby sa zaručilo, že každý varí len raz. Jeden najskúsenejší kuchár má na starosti hrniec, do ktorého vkladá všetky porcie a dáva tiež signál divochom, že môžu začať hodovať. Prebudenie kuchárov je implementované pomocou semaforu, konkrétne jeho nabitím na takú hodnotu, aký je počet všetkých kuchárov. Na zaručenie, že len jeden kuchár vloží jedlo do hrnca a dá signál divochom som požil mutex a counter. V kritickej oblasti zámku sa inkrementuje counter kuchárov. Keď všetci prácu dokončia hlavný kuchár vloží porcie do hrnca a dá signál divochom, že môžu začať hodovať.

### Pseudokód
```
def init():
    servings = 0
    cook_counter = 0

    cook_mutex = Mutex()
    savage_mutex = Mutex()
    barrier = Barrier(N_COOKS)
    empty_pot = Semaphore(0)
    full_pot = Semaphore(0)

 
    for savage_id in <0, N_SAVAGES - 1>:
        create_and_run_thread(savage, savage_id)
    for cook_id in <0, N_COOKS - 1>:
        create_and_run_thread(cook, cook_id)

def savage(savage_id):
    while True:
        savage_mutex.lock()
        print("divoch %2d: počet porcii v hrnci je %2d" % 
               (savage_id, servings))
        
        if servings == 0:
            print("divoch %2d: buím kuchárov" % savage_id)
            empty_pot.signal(N_COOKS)
            full_pot.wait()
        get_serving_from_pot(savage_id)
        savage_mutex.unlock()
        print("divoch %2d hoduje" % savage_id)
        sleep(rand(20 az 40 ms))

def get_serving_from_pot(savage_id):
    print("divoch %2d: beriem si porciu", savage_id)
    servings = servings - 1

def cook(cook_id):
    while True:
        empty_pot.wait()

        // varenie
        sleep(0.02 * N_SERVINGS + rand((0 az 3) / N_COOKS))

        barrier.wait()
        cook_mutex.lock()
        cook_counter += 1
        tmp_counter = dinner.cook_counter
        cook_mutex.unlock()

        if tmp_counter == N_COOKS:
            cook_counter = 0
            put_servings_in_pot(cook_id)
            full_pot.signal()

def put_servings_in_pot(cook_id):
    print("kuchár %2d: vkladá jedlo do hrnca" % cook_id)
    servings = N_SERVINGS
```
### Záver
Pri navrhovaní riešenia je doležíte premyslieť aký počet divochov, kuchárov a množstvo porcii nastaviť, aby bolo jednak varenie čo najefektívnejšie a zároveň aby divosi nemuseli dlho hladovať.
