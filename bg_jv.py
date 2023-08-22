#Lépe naformátovat historii kroků -- fstring pro lepší print
#


import random

pole = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] #navrh herniho pole
vyhazovac = [] #navrh vyhazovaciho pole

class Dices(): #hod kostkou
    def roll(self):
        roundRoll = [] #seznam hodu
        for i in range(2):
            roll = random.randint(1, 6)
            print(f"hod:{roll}")
            roundRoll.append(roll)

        if roundRoll[0] == roundRoll[1]: #double
            roundRoll.append(roundRoll[0])
            roundRoll.append(roundRoll[0])

        print(roundRoll)
        return roundRoll

class Kamen(): #klass kamene
    kamen_index = 0 #zaklad indexace kamenu pro následne mapovani
    seznamKameny = [] #seznam vsech vytvorenych kaminku podle indexu + barva

    def __init__(self,barva):
        Kamen.kamen_index += 1
        self.barva = barva
        self.index = f"{self.barva}_{Kamen.kamen_index}" #format indexace
        self.pozice = 0 #pozice kamene kvůli ná
        self.posun = 0
        self.preziti = 0
        self.historie = []
        if self.barva == 'white':
            self.pozice = 0
            print(self.barva, self.pozice)
        else:
            self.pozice = 0
            print(self.barva, self.pozice)
        Kamen.seznamKameny.append(self) #pridani do seznamu kamenu v poli

    def __str__(self):

        return f" barva: {self.barva}, index: {self.index}, pozice: {self.pozice}, preziti: {self.preziti}"

    def vyhozeni(self, roundRoll, lokace_kamene):
            print("musíš ho vyhodit")
            removed_item = pole[lokace_kamene].pop()
            vyhazovac.append(removed_item)
            print(f"VYHAZOVAC: {vyhazovac}")
            print(f"vyhozeny prvek: {removed_item}")
            pole[lokace_kamene].append(self.barva)
            self.pozice = lokace_kamene
            print(pole)

    def pohyb(self, roundRoll):  # basic pohyb
        print(f"{self}")

        for i in range(0, len(roundRoll)): #cyklus v delce hozenych hodnoot <2,4> podle hodnot
            tah = False
            pozice = int(self.pozice)
            if self.barva == 'white':
                print("Hraje bilej")
                posun = pozice + roundRoll[i]
            else:
                print("Hraje rudej")
                posun = pozice + roundRoll[i]
            print(f"posun: {posun}, {posun} + {roundRoll[i]}")
            if pole[posun] == self.barva or len(pole[posun]) == 0 and self.preziti == 0: #pokud tam mam stejnou barvu kamene nebo tam kamen neni tak vlozim šutrak
                print(f"posun pole:{posun}, pozice {self.pozice}")
                print(f"range pole:{range(len(roundRoll))}")
                pole[posun].append(self.barva) #pridam ho do pole
                self.pozice = posun
                self.preziti += 1
                self.historie.append(self.pozice)
                tah = True
            else:
                print("Jsem pred druhym posunem", len(pole[posun]))
                if pole[posun] == self.barva or len(pole[posun]) == 0:
                    print(f"pozice: {self.pozice}")
                    print(f"len pole:{len(pole[self.posun])}")
                    pole[self.pozice].pop()
                    pole[posun].append(self.barva) #pohnu s kamenem o pocet poli
                    self.pozice = posun
                    self.preziti += 1
                    self.historie.append(self.pozice)
                    tah = True


            print(pole) #vytisknu pole
                    #print(pole[posun][0], self.index)
            print(f"pole posun: {pole[posun][0]}, self index {self.barva}, posun pole {len(pole[posun])}, tah: {tah}")
            if pole[posun][0] != self.barva and len(pole[posun]) == 1 and tah is False and self.preziti == 0: #chtel jsem zautomatizovat pohyb, at nemusim vyvolat "vyhod kamen" ale vzdycky jen pohyb (pak se rozhodne)
                print("Jsem idiot a chci vyhazovat když nemám co")
                self.preziti += 1
                self.historie.append(self.pozice)
                self.vyhozeni(roundRoll, posun) #zavolam vyhozeni  roundRoll je muj hod kostkou, roundRoll[i] je ta pozice, kde doslo ke splneni tyhle podminky viz. nahore

            if pole[posun][0] != self.barva and len(pole[posun]) == 1 and tah is False: #chtel jsem zautomatizovat pohyb, at nemusim vyvolat "vyhod kamen" ale vzdycky jen pohyb (pak se rozhodne)
                print("Jsem idiot a chci vyhazovat když nemám co")
                pole[self.pozice].pop()
                self.historie.append(self.pozice)
                self.vyhozeni(roundRoll, posun) #zavolam vyhozeni  roundRoll je muj hod kostkou, roundRoll[i] je ta pozice, kde doslo ke splneni tyhle podminky viz. nahore


#class Hrac:

#    def __init__(self):
#        self.domecek =
#        self.barva =


"""
mam tam logickou chybu, ale tu uvidis hned co to zapnes. Vyhazujou se samovolne prvky a uz se mi nestackujou do pole jak predtim. Mama napicu nejakou podminku :)
"""

#-------------------------------------------------------------------------
#tvorba sutraku
w_kamen1 = Kamen("white")
w_kamen2 = Kamen("white")
w_kamen3 = Kamen("white")

r_kamen1 = Kamen("red")
r_kamen2 = Kamen("red")
r_kamen3 = Kamen("red")

#hra na 5 kol
for i in range(1):
    dice = Dices()
    hod = dice.roll()
    print(hod)
    w_kamen1.pohyb(hod)

    hod = dice.roll()
    r_kamen1.pohyb(hod)

#print indexu vsech kamenu
for i in Kamen.seznamKameny:
    print(i.index)