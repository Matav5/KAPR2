class Zvire:
    pocetZvirat = 0
    def __init__(self) -> None:
        print("Zavolal se Init")
        self.jeNazivu = True

    def jist(self):
        print("Já se napapal")


class Zirafa(Zvire):
    def __init__(self) -> None:
        self.jeNazivu = False

    def jist(self):    
        print("Našel jsem strom a pořádně jsem ho ožral")


class Kocka(Zvire):
    def jist(self):
        print("Chytnul jsem myš. Hrál jsem si s ní a teď mám svačinku")



zirafka = Zirafa()
Zvire.pocetZvirat+=1
kocicka = Kocka()

zviratko = Zvire()

kocicka.pocetZvirat += 1

Zvire.pocetZvirat+=5

mojeOblibeneZvire = zirafka

mojeOblibeneZvire.jeNazivu = True

seznamZvirat = list()

seznamZvirat.append(zirafka)
seznamZvirat.append(kocicka)
seznamZvirat.append(zviratko)


for zvireVSeznamu in seznamZvirat:
    zvireVSeznamu.jist()
    print(Zvire.pocetZvirat)
    print(zvireVSeznamu.pocetZvirat)
