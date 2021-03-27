# Cvičenie 6: Problém holičstva

Holičstvo pozostáva z dvoch miestnosti čakárne pre N klientov a miestnosti holíča, v prípade, že je čakáreň plná ďalší zákazník odchádza. Ak je holič obsadený a čakáreň nie je plná zákazník si sadne a čaká.

V úlohe je potrebné riešiť koordináciu medzi zákazníkmi a holičom. Riešenie je implementované pomocou dvoch vzájomných stretnutí dvoch vlákien (2x randezvous). Zákazník a holič sa musia synchronizovať pred strihaním a po dostrihaní. Obe stretnutia sú implementované pomocou semaforov. Pri prvom stretnutí čaká holič na príchod zákazníka a zákazník čaká na to kým bude holičom zavolaný. V druhom stretnutí holič čaká na signalizáciu zákazníka, že je s novým účesom spokojný a zákazník čaká na to aby ho holič prepustil zo stoličky.

V štandardnej implementácii so slabým semaforom (`barber_random_semaphore.py`) nie je zaručené poradie zákazníkov, na to aby bolo zaručené obslúženie zánikov v takom poradí v akom do holičstva prišli je potrebné použiť buď silný semafor (`barber_fifo_semaphore.py`) alebo queue (fifo fronta) slabých semaforov (`barber_queue.py`).
