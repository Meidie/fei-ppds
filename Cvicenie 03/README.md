# CviČenie 3: P-K experiment

V rámci experimentu som sa rozhodol pozorovať ako sa mení množstvo vyrobených produktov ak sa dynamicky mení počet producentov a čas produkcie. Staticky som následne menil hodnoty pre veľkosť úložiska, počet konzumentov a pozoroval zmeny vo výstupných dátach. Interval v ktorom sa menil čas výroby produktu bol v rozmedzí <0.01, 0.1> s krokom 0.01. Interval počtu producentov sa pohyboval v rozmedzí od 1 po 10 s krokom 1.


1. Prvý experiment

Čas produkcie výrobku | Počet producentov | Čas spracovania výrobku | Počet konzumentov | Veľkosť úložiska 
--------------------- | ------------------|-------------------------|-------------------|-----------------
<0.01, 0.1>| <1, 10>| randint(0, 10) / 200 | 10 | 10


![Alt text](/Cvicenie%2003/graphs/WC10C10.png?raw=true "")

2. Druhý experiment

Čas produkcie výrobku | Počet producentov | Čas spracovania výrobku | Počet konzumentov | Veľkosť úložiska 
--------------------- | ------------------|-------------------------|-------------------|-----------------
<0.01, 0.1>| <1, 10>| randint(0, 10) / 200 | 10 | 5


![Alt text](/Cvicenie%2003/graphs/WC5C10.png?raw=true "")

3. Tretí experiment

Čas produkcie výrobku | Počet producentov | Čas spracovania výrobku | Počet konzumentov | Veľkosť úložiska 
--------------------- | ------------------|-------------------------|-------------------|-----------------
<0.01, 0.1>| <1, 10>| randint(0, 10) / 200 | 10 | 20


![Alt text](/Cvicenie%2003/graphs/WC20C10.png?raw=true "")

V prvých troch experimentoch som sa sústredil na zmenu veľkosti úložiska. Na grafoch vidíme, že množstvo vyrobených produktov stúpa so znížením času produkcie a zvýšením počtu producentov, teda presne tak ako by sme očakávali. Rovnako môžeme vidieť, že čim väčšiu kapacitu má úložisko tým vieme aj viacej produktov vyrobiť. Experiment pri ktorom bol sklad najväčší však nie je úplne optimálny z hľadiska využitia zdrojov. Ak by sme napríklad chceli vyrábať 300 výrobkov vhodnejšie by bolo úložisko s menšou kapacitou pretože by sme mohli mať menej producentov.

4. Štvrtý experiment

Čas produkcie výrobku | Počet producentov | Čas spracovania výrobku | Počet konzumentov | Veľkosť úložiska 
--------------------- | ------------------|-------------------------|-------------------|-----------------
<0.01, 0.1>| <1, 10>| randint(0, 10) / 200 | 20 | 10


![Alt text](/Cvicenie%2003/graphs/WC10C20.png?raw=true "")

5. Piaty experiment

Čas produkcie výrobku | Počet producentov | Čas spracovania výrobku | Počet konzumentov | Veľkosť úložiska 
--------------------- | ------------------|-------------------------|-------------------|-----------------
<0.01, 0.1>| <1, 10>| randint(0, 10) / 200 | 5 | 10


![Alt text](/Cvicenie%2003/graphs/WC10C5.png?raw=true "")

6. Šiesty experiment

Čas produkcie výrobku | Počet producentov | Čas spracovania výrobku | Počet konzumentov | Veľkosť úložiska 
--------------------- | ------------------|-------------------------|-------------------|-----------------
<0.01, 0.1>| <1, 10>| randint(0, 10) / 200 | 20 | 5


![Alt text](/Cvicenie%2003/graphs/WC5C20.png?raw=true "")

V ďalších experimentoch som sa zameral už aj na zmenu počtu konzumentov. Väčšie množstvo konzumentov eliminuje nutnosť mať väčšie úložisko čo znamená, že producenti môžu vyrábať nové produkty rýchlejšie a tiež ich môže byť aj menej vďaka čomu sa dajú znížiť celkove náklady na prevádzku. 

### Záver

Na základe týchto experimentov je možné vidieť, že ak získame väčšie množstvo konzumentov nebudeme nutne musieť investovať do väčšieho úložiska pretože ak je odber vyšší producenti môžu viacej vyrábať bez toho aby museli čakať na uvoľnenie skladu. Pri veľkom počte konzumentov a malom úložisku by sme však potrebovali aj viacej producentov aby sme splnili dopyt a v takom prípade je lepšie investovať do zväčšenia úložiska než do ďalších producentov. Celkovo je teda doležíte neustále upravovať kapacitu úložiska a počet producentov na základe toho koľko mame konzumentov.
