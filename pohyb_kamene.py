import pygame
from matav import Kamen, Hrac, Policko, Hra
from dice import HerniKostky

#Class Hra:

##Jsem ve hře!!!!

#!!!Vymyslet kam má jít, správně popovat možnosti z kostky, možnost volby tahu!!!
#
def pohybKamene(self, Kamen, HerniKostky):
    """
    Pohyb kamene po herním poli
    :param self:
    :param HerniKostky:
    :return:
    """
    kostky = HerniKostky.hod
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for index in enumerate(Hra.herniPole):
                souradnice = tuple[index.pozice.x, index.pozice.y]
                if souradnice.rect.collidepoint(mouse_x, mouse_y) and index in Hra.vypisTahyPolicek(kostky):
                    tah = index
                    if Policko.vlastnikPolicka(tah) == Hra.hracNaRade(clovekHrac) or policko.posledniKamen(tah) == 1:
                        cil = Kamen.souradnice + tah
                        Policko.odeberKamen()
                        Policko.pridejKamen(cil, vybranyKamen)







    # len(range(start, cil)) # rozdil indexu mezi původní pozicí a cílovou pozicí

# potřebuju kontrolovat, zda nepřelejzám přes kostku (hod)
#musím umožnit volbu !!kombinace!! pro pohyb
