def cat(f, next_fnc):
    """Obycajna funkcia, cita subor riadok po riadku.

    Kazdy riadok posle na spracovanie koprogramu next_fnc().
    Po skonceni citania riadkov vstupneho suboru ukonci cinnost
    generatora, ktoremu posiela udaje.
    Funkcia close() generatoru posle vynimku GeneratorExit.
    """
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def grep(substring, next_fnc):
    """Koprogram, ktory caka na vstupny riadok textu zo suboru
    Akonahle ziska riadok, dalsiemu koprogramu posiela pocet vyskytov
    podretazca `substring` v danom riadku.
    Po prijati vynimky GeneratorExit tuto vynimku preposle
    koprogramu, ktory spracuva pocet vyskytov podretazca.
    """
    try:
        while True:
            line = (yield)
            next_fnc.send(line.count(substring))
    except GeneratorExit:
        next_fnc.close()


def wc(substring):
    """Koprogram, ktory caka na pocet vyskytov podretazca v riadku.

    Akonahle dostane pocet, pripocitava ho k celkovemu vysledku.
    Po obdrzani vynimky GeneratorExit cinnost koprogramu konci
    vypisom vysledku na obrazovku.
    """
    n = 0
    try:
        while True:
            n += (yield)
    except GeneratorExit:
        print(substring, n, flush=True)


def dispatch(greps):
    """Koprogram, ktoreho ulohou je distribuovat riadok ziskany
    z funkcie cat() medzi vsetky koprogramy, ktore ma ulozene
    vo vstupnom zozname `greps`.
    """
    try:
        while True:
            line = (yield)
            for grep in greps:
                grep.send(line)
    except GeneratorExit:
        for grep in greps:
            grep.close()


def main():
    f = open("text.txt", "r")
    substrings = ["to", "that", "the", "as"]
    greps = []

    for substring in substrings:
        w = wc(substring)
        next(w)
        g = grep(substring, w)
        next(g)
        greps.append(g)

    d = dispatch(greps)
    next(d)
    cat(f, d)

    f.close()


if __name__ == "__main__":
    main()
