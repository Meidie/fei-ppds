# Cvičenie 9: CUDA pomocou Numba

V súbore `cuda_prime.py` sa nachádza jednoduchý program, ktorý rozhoduje o tom či sú alebo nie sú dané čísla prvočíslami. 
Vstupne čísla sú generované náhodne v počte 320, pričom môžu byť v rozpätí od 1 000 000 do 9 999 999 999 999. 
Vlákien rámci jedného bloku je 32 a blokov je 10. Výsledky rozhodovania sa ukladajú do ```dictionary``` , ktorý je jedným zo vstupných parametrov funkcie spolu so samotnými dátami.
