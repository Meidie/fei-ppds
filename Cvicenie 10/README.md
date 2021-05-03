# Cvičenie 10: CUDA prúdy a udalosti

V súbore `cuda_prime_stream.py` sa nachádza jednoduchý program, ktorý rozhoduje o tom či sú alebo nie sú dané čísla prvočíslami. 

Riešenie z predchádzajúceho týždňa bolo prerobené tak aby boli využité prúdy, v dôsledku čoho boli vytvorené viaceré polia výpočtov. Program na začiatku vygeneruje 5 polí. Každé pole obsahuje 64 náhodných čísiel. Každému poľu je priradený jeden stream. V predvolenom nastavení grid v každom z kernelov obsahuje 2 bloky po 32 vlákien. 

Žiaľ nemám k dispozícii grafickú kartu, na ktorej by som mohol robiť výpočty priamo, použil som preto pri implementácii emulátor v dôsledku čoho použitie udalostí na meranie času nebolo možné. Na meranie času som teda použil ```perf_counter()``` z modulu time.

#### Záver

Vzhľadom na to, že vstupné dáta sú generované náhodne neviem s určitosťou povedať či došlo k zrýchleniu vykonávania programu, ale po niekoľkých opakovaných spusteniach sa výsledky pohybovali v približne rovnakom rozpätí s výkyvmi do 1 sekundy.
