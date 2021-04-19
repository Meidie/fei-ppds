# Cvičenie 8: Asynchrónne programovanie

Cieľom aplikácie je vyhľadávať najväčšie prvočíslo pod zadanou hranicou.
Prednastavené hodnoty sú: [100000, 10000, 1000, 10, 18, 17].

V súbore `prime.py` sa nachádza synchrónna implementácia. Celkový čas vykonávanie programu: **11.3s** 

#### Výstup synchrónnej implementácie:
```
Highest prime below 100000
→ Highest prime below 100000 is 99991
Highest prime below 1000
→ Highest prime below 1000 is 997
Highest prime below 18
→ Highest prime below 18 is 17
Highest prime below 10000
→ Highest prime below 10000 is 9973
Highest prime below 17
→ Highest prime below 17 is 13
Highest prime below 100
→ Highest prime below 100 is 97
Total elapsed time:  11.3
```

V súbore `prime_async.py` sa nachádza asynchrónna implementácia. Celkový čas vykonávanie programu: **5.2s** 

#### Výstup asynchrónnej implementácie:
```
Highest prime below 100000
Highest prime below 10000
Highest prime below 1000
Highest prime below 100
Highest prime below 18
Highest prime below 17
→ Highest prime below 18 is 17
→ Highest prime below 17 is 13
→ Highest prime below 100 is 97
→ Highest prime below 1000 is 997
→ Highest prime below 10000 is 9973
→ Highest prime below 100000 is 99991
Total elapsed time:  5.2
```

#### Záver

Z časových výsledok je možné vidieť, že asynchrónna implementácia je rýchlejšia ako synchrónna.
Pri synchrónnej implantácii sa jednotlivé tasky vykonávajú jeden po druhom, pri asynchrónnej implementácii sa môžu tasky vykonávať konkurentne keďže nedochádza k blokovaniu behu programu, ale len samostatných taskov, čo znamená, že ak je jeden task blokovaný ďalšie môžu pokračovať.

Pri menších prednastavených hodnotách by bol výsledný časový rozdiel malý a do istej mieri až zanedbateľný. Naopak pri väčších prednastavených hodnotách by sa rozdiel nestále zväčšoval v prospech asynchrónnej implementácie.

