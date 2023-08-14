import random

class Kostka():

    def __init__(self, hrany = 6):
        self.hrany = hrany
        self.hodnota = 1

    def hod(self):
        self.hodnota = random.randint(1, self.hrany)
        return self.hodnota


class HerniKostky():

    def __init__(self):
        self.kostky = [Kostka(), Kostka()]
        self.historie = []

    def hod(self):
        seznam_hodnot = []
        i = 0
        for kostka in self.kostky:
            hondnota_hodu = kostka.hod()
            seznam_hodnot.append(hondnota_hodu)
            self.historie.append(hondnota_hodu)

        if seznam_hodnot[i] == seznam_hodnot[i+1]:
            seznam_hodnot.append(seznam_hodnot[i])
            seznam_hodnot.append(seznam_hodnot[i])

        return seznam_hodnot


moje_kostka = HerniKostky()
hodnoty = moje_kostka.hod()

print(f"Hodnota kostek je: {hodnoty}")
print(moje_kostka.historie)


