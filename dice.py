import random

class Kostka():

    def __init__(self, strany = 6):
        self.strany = strany
        self.hodnota = list()


    def hod(self):
        self.hodnota = random.randint(1, self.strany)
        return self.hodnota


class HerniKostky():

    def __init__(self):
        self.kostky = [Kostka(), Kostka()]
        self.historie = []
        self.seznamHodnot = []
        self.hodilKostkou = False

    def hod(self):
        if not self.hodilKostkou:
            i = 0
            for kostka in self.kostky:
                hondnota_hodu = kostka.hod()
                self.seznamHodnot.append(hondnota_hodu)
                self.historie.append(hondnota_hodu)
            self.hodilKostkou = True

            if self.seznamHodnot[i] == self.seznamHodnot[i+1]:
                self.seznamHodnot.append(self.seznamHodnot[i])
                self.seznamHodnot.append(self.seznamHodnot[i])

            return self.seznamHodnot

        else:
            print(f"Hráč kostkou již hodil.")

