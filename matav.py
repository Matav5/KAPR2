
from collections import deque
from numbers import Number
from dice import HerniKostky




class Pozice:
    '''
    !! Pozor na REFERENCE !!
    Pomocná třída pro určení pozice -> slouží hlavně pro grafické zobrazení
    '''
    def __init__(self,x : Number,y : Number) -> None:
        self.x = x
        self.y = y

    
    def nastav(self, x:Number, y: Number):
        '''
        vezme pozici a přepíše jí X a Y
        '''
        self.x = x
        self.y = y
    
    def pohni(self, x:Number, y: Number):
        '''
        vezme pozici a pohne jí o X a Y
        '''
        self.x += x
        self.y += y


    def __eq__(self, __value: object) -> bool:
        if __value is Pozice:
            return __value.x == self.x and __value.y == self.y
        return False       

          
class Hrac:
    '''
    Třída pro hráče obsahující domeček sloužící k rozlišování kdo hraje a koho je co
    '''
    def __init__(self, poziceDomecku : Pozice) -> None:
        self.domecek = Domecek(Pozice(poziceDomecku.x,poziceDomecku.y))
   
class Kamen:
    '''
    Třída pro kámen s historií (zásobník) s hráčem který kámen vlastní pozicí pro grafické zobrazení
    '''
    def __init__(self, hrac: Hrac) -> None:
        self.historie = deque()
        self.pozice = Pozice(0,0)
        self.hrac = hrac

class Policko:
    '''
    Třída pro políčka obsahující zásobník kamenů a pozici pro grafické zobrazení
    '''
    def __init__(self, x,y) -> None:
        self.pozice = Pozice(x,y)
        self.kameny = deque()

    def pridejKamen(self,kamen:Kamen) -> None:
        kamen.pozice = self.pozice 
        self.kameny.append(kamen)
    
    def __str__(self) -> str:
        return str(len(self.kameny))

class Bar:
    '''
    Třída pro bar sloužící jako vytvářeč pro zničené kameny s pozicí pro grafické zobrazení
    '''
    def __init__(self, pozice : Pozice) -> None:
        self.pozice = pozice
        self.vyrobeneKameny = deque()
    def vyrobKamen(self) -> Kamen:
        kamen =  Kamen(self.pozice)
        self.vyrobeneKameny.append(
            kamen
            )
        return kamen
    def vemKamen(self) -> Kamen:
        return self.vyrobeneKameny.pop()
    

class Domecek:
    '''
    Třída pro domeček sloužící jako cíl pro Hráče s pozicí pro grafické zobrazení
    '''
    def __init__(self, pozice) -> None:
        self.pozice = pozice
        self.kamenyVDomecku = deque()

    def schovejKamen(self, kamen:Kamen) -> Kamen:
        self.kamenyVDomecku.append(
            kamen
            )
    def ziskejPocet(self) -> Number:
        return len(self.kamenyVDomecku)
        
class Hra:
    '''
    Třída hry která při vytvoření vytvoří herní pole, vloží kameny a nastaví hráče podle parametrů -> bude sloužit jako základní stavební kámen hry
    '''
    def __init__(self, cervenyHrac : Hrac, bilyHrac : Hrac) -> None:
        self.dvojKostka = HerniKostky()
        self.cervenyHrac = cervenyHrac
        self.bilyHrac = bilyHrac
        self.herniPole = []
        self.vygenerujPole()
        self.vlozKameny()
        for x in self.herniPole:
            print(x, end=" ")

        #Implementovat rozhodnutí pořadí kostkou
        self.aktualniHrac = cervenyHrac
    
    #viz obrázek ./pomocnyMaterial/deskaLayout.png
    def vlozKameny(self):
        self.vlozKamenyNaSloupci(self.cervenyHrac,self.bilyHrac, 0,5)
        self.vlozKamenyNaSloupci(self.bilyHrac,self.cervenyHrac, 4,3)
        self.vlozKamenyNaSloupci(self.bilyHrac,self.cervenyHrac, 6,5)
        self.vlozKamenyNaSloupci(self.cervenyHrac,self.bilyHrac, 11,2)

    def vlozKamenyNaSloupci(self, hracPrvniRadek : Hrac,hracDruhyRadek : Hrac, sloupec: Number, pocet: Number):
        for i in range(0,pocet):
            self.herniPole[sloupec].pridejKamen(Kamen(hracPrvniRadek)) 
            self.herniPole[sloupec + 11].pridejKamen(Kamen(hracDruhyRadek))

        
    def vytvorRadu(self,seznamPolicek,zacX,zacY,pocet,smer, velPol = 90): 
        for i in range(pocet):
            seznamPolicek.append(Policko(zacX +  i * velPol * smer ,zacY ))

    def vygenerujPole(self):
        '''
            Vytvoří a vloží políčka !!!! Je potřeba je správně napozicovat !!!!
        '''
        policka = list()
        self.vytvorRadu(policka,1400,250,6,-1)
        self.vytvorRadu(policka,800,250,6,-1)
        self.vytvorRadu(policka,350,875,6,1)
        self.vytvorRadu(policka,950,875,6,1)
        # x 350 350
        # y 250 875 
        #mezi polema 
        #bar 50 px
        i = 0
        for policko in policka:
            i+=1
            print(f"Poličko ({i}) na poz: X: {policko.pozice.x} Y:{policko.pozice.y}")
        self.herniPole = policka

    def vypisTah(self):
        '''
            Vypíše všechny aktuální možné tahy (graficky)
        '''
        pass
    def prepniHrace(self):
        if self.aktualniHrac == self.cervenyHrac:
            self.aktualniHrac = self.bilyHrac 
        else:
            self.aktualniHrac = self.cervenyHrac
    
hra = Hra(Hrac(Pozice(100,100)),Hrac(Pozice(100,200)))
print(hra.herniPole)