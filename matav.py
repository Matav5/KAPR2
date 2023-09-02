
from collections import deque
from numbers import Number
from typing import List
from pygame import Rect, Surface, image
import pygame
from pygame.sprite import Group,Sprite
from dice import HerniKostky
from pygame.event import Event

invisibleImage = pygame.Surface((32, 32), pygame.SRCALPHA)
invisibleImage.fill((0, 0, 0, 0)) 

class ObrazkovySprite(Sprite):
    def __init__(self, x, y , obrazek_cesta: str,*groups: Group) -> None:
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.image = image.load(obrazek_cesta)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

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
    def __str__(self) -> str:
        return f"X: {self.x} Y: {self.y}"
          
class Hrac:
    '''
    Třída pro hráče obsahující domeček sloužící k rozlišování kdo hraje a koho je co
    '''
    def __init__(self, obrazek, *groups : Group) -> None:
        self.groups = groups
        self.domecek = None
        self.bar = None
        self.smer = None
        self.obrazek = obrazek
    def nastavDomecekABar(self, poziceDomecku: Pozice, poziceBaru : Pozice):
        self.domecek = Domecek(poziceDomecku,self)
        self.bar = Bar(poziceBaru,self)
   
class Kamen(Sprite):
    '''
    Třída pro kámen s historií (zásobník) s hráčem který kámen vlastní pozicí pro grafické zobrazení
    '''
    def __init__(self, hrac: Hrac) -> None:
        super().__init__(hrac.groups)
        self.souradnice = 2**32
        self.historie = deque()
        self.pozice = Pozice(0,0)
        self.hrac = hrac
        self.image = image.load(hrac.obrazek)
        self.rect = self.image.get_rect()
        self.rect.center = [0,0]        
    def updateGrafiku(self):
        self.rect.center = (self.pozice.x,self.pozice.y)     

class Policko(Sprite):
    '''
    Třída pro políčka obsahující zásobník kamenů a pozici pro grafické zobrazení
    '''
    def __init__(self,souradnice, x,y, *groups :Group) -> None:
        super().__init__(groups)
        self.souradnice = souradnice
        self.pozice = Pozice(x,y)
        self.kameny = deque()
        self.rect = Rect(0,0,0,0)
        self.rect.height = 300
        self.rect.width = 90
        self.rect.center = (x,y)
        self.image = invisibleImage
    def pridejKamen(self,kamen:Kamen) -> None:
        kamen.pozice = Pozice(self.pozice.x, self.pozice.y + kamen.rect.width/1.5 * len(self.kameny))
        kamen.souradnice = self.souradnice 
        kamen.updateGrafiku()
        self.kameny.append(kamen)
    def odeberKamen(self) -> Kamen:
        try:
            kamen = self.kameny.pop()
            kamen.pozice = Pozice(10000,10000)
            kamen.souradnice = 300000000000
            return kamen
        except:
            return None
    def __str__(self) -> str:
        return str(len(self.kameny))
    
    def maKamen(self)->bool:
        return len(self.kameny) > 0

    def daSeSebratKamen(self)->bool:
        return len(self.kameny) == 1
    
    def posledniKamen(self) -> Kamen:
        if not self.maKamen():
            return None
        return self.kameny[len(self.kameny)-1]
    
    def vlastnikPolicka(self) -> Hrac:
        if not self.maKamen():
            return None   
        return self.posledniKamen().hrac
    

class Bar(Sprite):
    '''
    Třída pro bar sloužící jako vytvářeč pro zničené kameny s pozicí pro grafické zobrazení
    '''
    def __init__(self, pozice : Pozice, hrac : Hrac) -> None:
        super().__init__(hrac.groups)
        self.hrac = hrac
        self.pozice = pozice
        self.rect = Rect(0,0,0,0)
        self.rect.width = 80
        self.rect.height = 300
        self.rect.center = (pozice.x,pozice.y)
    
        self.vyrobeneKameny = deque()
        self.image = invisibleImage

    def vyrobKamen(self) -> Kamen:
        kamen =  Kamen(self.hrac)
        kamen.pozice = Pozice(self.pozice.x, self.pozice.y + kamen.rect.width/1.5 * len(self.vyrobeneKameny))
        kamen.updateGrafiku()
        self.vyrobeneKameny.append(
            kamen
            )
        return kamen
    
    def vemKamen(self) -> Kamen:
        return self.vyrobeneKameny.pop()
    

class Domecek(Sprite):
    '''
    Třída pro domeček sloužící jako cíl pro Hráče s pozicí pro grafické zobrazení
    '''
    def __init__(self, pozice, hrac : Hrac) -> None:
        super().__init__(hrac.groups)
        self.hrac = hrac
        self.pozice = pozice
        self.kamenyVDomecku = deque()
        self.rect = Rect(0,0,0,0)
        self.rect.width = 80
        self.rect.height = 300
        self.rect.center = (pozice.x,pozice.y)
        self.image = invisibleImage
        

    def schovejKamen(self, kamen:Kamen) -> Kamen:
        self.kamenyVDomecku.append(
            kamen
            )
    def ziskejPocet(self) -> Number:
        return len(self.kamenyVDomecku)
class Tah:
    def __init__(self,kamen : Kamen,policko : Policko, pohyby : list) -> None:
        self.kamen = kamen
        self.policko = policko
        self.pohyby = pohyby
             
class Hra:
    '''
    Třída hry která při vytvoření vytvoří herní pole, vloží kameny a nastaví hráče podle parametrů -> bude sloužit jako základní stavební kámen hry
    '''
    def __init__(self, cervenyHrac : Hrac, bilyHrac : Hrac, *groups : Group) -> None:
        self.groups = groups
        self.dvojKostka = HerniKostky()
        self.cervenyHrac = cervenyHrac
        self.cervenyHrac.smer = 1
        self.cervenyHrac.nastavDomecekABar(Pozice(1550,310),Pozice(875,310))

        self.bilyHrac = bilyHrac
        self.bilyHrac.smer = -1
        self.bilyHrac.nastavDomecekABar(Pozice(1550,760),Pozice(875,760))

        self.herniPole = []
        self.vygenerujPole()
        self.vlozKameny()
      
        #TODO Implementovat rozhodnutí pořadí kostkou
        self.aktualniHrac = cervenyHrac
    
    #viz obrázek ./pomocnyMaterial/deskaLayout.png
    def vlozKameny(self):
        self.vlozKamenyNaSloupci(self.cervenyHrac,self.bilyHrac, 11,5)
        self.vlozKamenyNaSloupci(self.bilyHrac,self.cervenyHrac, 7,3)
        self.vlozKamenyNaSloupci(self.bilyHrac,self.cervenyHrac, 5,5)
        self.vlozKamenyNaSloupci(self.cervenyHrac,self.bilyHrac, 0,2)

    def vlozKamenyNaSloupci(self, hracPrvniRadek : Hrac,hracDruhyRadek : Hrac, sloupec: Number, pocet: Number):
        for i in range(0,pocet):
            indexHorni = sloupec
            indexSpodni = len(self.herniPole)-1-sloupec
            self.herniPole[indexHorni].pridejKamen(Kamen(hracPrvniRadek)) 
            self.herniPole[indexSpodni].pridejKamen(Kamen(hracDruhyRadek))

        
    def vytvorRadu(self,seznamPolicek,zacX,zacY,pocet,smer, velPol = 90): 
        for i in range(pocet):
            seznamPolicek.append(Policko(len(seznamPolicek),zacX +  i * velPol * smer ,zacY, self.groups ))

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


    def vypisTahyPolicek(self,kostky) -> list():
        '''
        Výpis možností pro hráče
        '''
        moznePolicka = list()
        for index,policko in enumerate(self.herniPole):
            if not policko.maKamen():
                continue
            elif policko.maKamen() and policko.vlastnikPolicka() != self.aktualniHrac:
                continue
            else:
               moznePolicka.extend(self.vypisTah(kostky,index))
        return moznePolicka

    def vypisTah(self, kostky : list, policko : int) -> list():
        '''
        Výpis pro specifické políčko
        '''
        kamen = self.herniPole[policko].posledniKamen()
        moznePolicka = list()
        for index, kostka in enumerate(kostky):
            # for soucet in range(index,0,-1):
            cil = policko+kostka * kamen.hrac.smer
            if cil <= 0 or cil >= len(self.herniPole):
                continue
            moznePolicko = self.herniPole[cil]
            if moznePolicko.vlastnikPolicka() == None or moznePolicko.vlastnikPolicka() == kamen.hrac:
                moznePolicka.append(Tah(kamen,moznePolicko,kostka))
            else:
                print(f"{kamen.souradnice} na pozici: {cil}  Vlastní Opponent: {moznePolicko.vlastnikPolicka() != None and moznePolicko.vlastnikPolicka() != kamen.hrac}")

            kombinace = list()
            for IndexKomboKostek in range(index,-1,-1):
                kombinace.append(kostky[IndexKomboKostek])
                cil = policko + sum(kombinace) * kamen.hrac.smer
                if cil <= 0 or cil >= len(self.herniPole):
                    continue
                moznePolicko = self.herniPole[cil]
                if (moznePolicko.vlastnikPolicka() == None or moznePolicko.vlastnikPolicka() == kamen.hrac) and not (kamen,moznePolicko) in moznePolicka:
                    moznePolicka.append(Tah(kamen,moznePolicko,kombinace))
                else:
                    print(f"{kamen.souradnice} na pozici: {cil}  Vlastní Opponent: {not(moznePolicko.vlastnikPolicka() == None or moznePolicko.vlastnikPolicka() == kamen.hrac)} a je v seznamu: {(kamen,moznePolicko) in moznePolicka}")
          
            kombinace = list()
            for IndexKomboKostek in range(0, index, 1):
                kombinace.append(kostky[IndexKomboKostek])
                cil = policko + sum(kombinace) * kamen.hrac.smer
                if cil <= 0 or cil >= len(self.herniPole):
                    continue
                moznePolicko = self.herniPole[cil]
                if (moznePolicko.vlastnikPolicka() == None or moznePolicko.vlastnikPolicka() == kamen.hrac) and not (kamen,moznePolicko) in moznePolicka:
                    moznePolicka.append(Tah(kamen,moznePolicko,kombinace))
                else:
                    print(f"{kamen.souradnice} na pozici: {cil}  Vlastní Opponent: {not(moznePolicko.vlastnikPolicka() == None or moznePolicko.vlastnikPolicka() == kamen.hrac)} a je v seznamu: {(kamen,moznePolicko) in moznePolicka}")
   

        return moznePolicka

    def hracNaRade(self,hrac) -> bool:
        return hrac == self.aktualniHrac
    def prepniHrace(self):
        if self.aktualniHrac == self.cervenyHrac:
            self.aktualniHrac = self.bilyHrac 
        else:
            self.aktualniHrac = self.cervenyHrac
        #TODO Pokud hráč bude AIHrac => zavolá funkci Hraj(hra)

    def update(self, event: List[Event]):
        for group in self.groups:
            for sprite in group:
                if sprite.rect.collidepoint(event.pos):
                    if type(sprite) is Policko:
                        print(self.vypisTah(self.dvojKostka.hod(), -1))
                        print(f"Políčko !! {type(sprite)}")
                        break
                        # TODO zjistit jak ošetřit, že již je políčko vybrané a chceme kliknout na higlightované - příznak?
                    elif type(sprite) is Bar and len(sprite.vyrobeneKameny) >= 1:
                        for kamen in sprite.vyrobeneKameny:
                            if kamen.hrac == self.aktualniHrac:
                                if self.hracNaRade(self.aktualniHrac) == self.cervenyHrac:
                                    self.vypisTah(self.dvojKostka.hod(), -1)
                                else:
                                    self.vypisTah(self.dvojKostka.hod(), 25)

                                # TODO podivej se, jestli má hráč na tahu kameny na baru, pokud ano, neumožni mu hrát jiný kámen
                    elif type(sprite) is Domecek:  # Je to domeček
                        print(f"Domeček !!! {type(sprite)}")

                        # TODO navrhni kontrolu domečku hráče - zda tam může jít -- všechny kameny ve 4. segmentu -- checkování zda je domeček full ve hře
   
   
   
    def pohniKamen(self, kamen : Kamen, cil : Policko):
        pass
   
    def maHracKamenyVeCtvrtymSegmentu(self, hrac : Hrac) -> bool:
        if hrac.smer == 1:
            startIndex = 23
        else:
            startIndex = 0
        endIndex = startIndex - 6 * hrac.smer
        pocetKamenu = 0
        for souradnice in range(startIndex, endIndex, -hrac.smer):
            if self.herniPole[souradnice].vlastnikPolicka() == hrac:
                pocetKamenu += len(self.herniPole[souradnice].kameny)
        print(pocetKamenu)
        return pocetKamenu == 15
    # Když bude v baru více než jeden, musíš ho vybrat a pokud ho vybereš, ukáže políčka z baru --
    
class AIHrac(Hrac):
        def __init__(self, obrazek, *groups : Group) -> None:
         super().__init__(obrazek, groups)
        def hraj(self, hra : Hra):
            '''
            AI hraje agresivně. Pokud uvidí osamocený kámen jde po něm jak slepice po flusu!
            Pokud se dostane do 4. segmentu AI se snaží dostat se do domečku.
            AI se snaží chránit si kameny. Pokud bude mít možnost tak se pokusí se svůj kámen ochránit dalším
            Jinak se snaží dostat co nejdál 
            '''
            if hra.aktualniHrac != self:
                return
            while len(hra.dvojKostka.seznamHodnot) > 0 and hra.dvojKostka.hodilKostkou:
                tahy = hra.vypisTahyPolicek(hra.dvojKostka.seznamHodnot)
                #Pokud nemá tahy ukončí kolo
                if len(tahy) == 0:
                    return
                nejlepsiTah = tahy[0] 
                for tah in tahy:
                    #Zjistí jestli tah má v cíli protivníka který má jen jeden kámen => pokud ano ihned se tam pohne a pokračuje dalším tahem
                    if tah.policko.vlastnikPolicka != self and tah.policko.daSeSebratKamen():
                        nejlepsiTah = tah
                        break
                    #Pokud má všechny kameny na konci => snaží se ty nejvzdálenější možné kameny nacpat do domečku
                    elif hra.maHracKamenyVeCtvrtymSegmentu(self):
                        #smer 1 od shora dolů
                        if self.smer == 1:
                            if nejlepsiTah.souradnice <= 23 and nejlepsiTah.policko.souradnice < tah.policko.souradnice:
                                nejlepsiTah = tah
                                if nejlepsiTah >= 24:
                                    break
                        else:
                             if nejlepsiTah.souradnice >= 0 and nejlepsiTah.policko.souradnice > tah.policko.souradnice:
                                nejlepsiTah = tah
                                if nejlepsiTah <= 0:
                                    break
                    #Pokud má osamocený kámen snaží se ho ochránit
                    elif self.osamocenyKamen(hra,tah):
                        nejlepsiTah = tah
                        break
                    #Pokud nic jiného nevyjde
                    else:
                        if self.smer == 1:
                           if tah.kamen.souradnice < nejlepsiTah.kamen.souradnice:
                               nejlepsiTah = tah
                        else:
                            if tah.kamen.souradnice > nejlepsiTah.kamen.souradnice:
                               nejlepsiTah = tah
                hra.dvojKostka.seznamHodnot.remove(abs(nejlepsiTah.kamen.souradnice - nejlepsiTah.policko.souradnice) )
                #TODO udělat funkci pohni Kamen
                hra.pohniKamen(nejlepsiTah.kamen, nejlepsiTah.policko)

        def osamocenyKamen(self, hra : Hra, tah : tuple) -> bool:
            vybranePolicko = hra.herniPole[tah.kamen.souradnice]
            if vybranePolicko is Policko:
                return False
            return vybranePolicko.daSeSebratKamen()


                     
'''
ai = AIHrac("red_front_side.png")
hra = Hra(ai,Hrac("white_front_side.png"))
hra.dvojKostka.hod()
hra.dvojKostka.seznamHodnot.clear()
hra.dvojKostka.seznamHodnot.append(5)
hra.dvojKostka.seznamHodnot.append(6)
print(hra.dvojKostka.seznamHodnot)
ai.hraj(hra)
hra.prepniHrace()

print(hra.maHracKamenyVeCtvrtymSegmentu(hra.aktualniHrac))
kostky = (4,4,4,4)
print(kostky)
moznosti = hra.vypisTahyPolicek(kostky)
for moznost in moznosti:
    print(f"{moznost[0].hrac} {moznost[0].souradnice} -> {moznost[1].souradnice}")
'''



'''
hra.aktualniHrac.bar.vyrobKamen()
    hra.prepniHrace()
    if hra.hracNaRade(clovekHrac):
        for sprite in vykreslovaci_group:
            if sprite.rect.collidepoint(event.pos):
                print(type(sprite))
                if type(sprite) is Policko:
                       
                            
                    print("Poličko")
                if type(sprite) is Kamen:
                    print("Kamen")
'''
