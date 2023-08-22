
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
    def __init__(self, pozice : Pozice) -> None:
        self.pozice = Pozice(pozice.x,pozice.y)
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
        for y in self.herniPole:
            print("\n")
            for x in y:
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
            self.herniPole[0][sloupec].pridejKamen(Kamen(hracPrvniRadek)) 
            self.herniPole[1][sloupec].pridejKamen(Kamen(hracDruhyRadek))



    def vygenerujPole(self):
        '''
            Vytvoří a vloží políčka !!!! Je potřeba je správně napozicovat !!!!
        '''
        for y in range(0,2):
            self.herniPole.append([])
            for x in range(0,12):
                self.herniPole[y].append(Policko((y*500,x*50)))

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
    
hra = Hra(Hrac(),Hrac())
