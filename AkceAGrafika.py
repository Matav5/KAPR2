import pygame
from pygame.sprite import  Sprite, Group
from matav import Policko, Kamen, Hra, Hrac, Pozice
class Akce:
    def __init__(self) -> None:
        self.seznamFunkci = list()

    def pridejAkci(self, funkce) -> None:
        self.seznamFunkci.append(funkce)

    def zavolejAkci(self, args):
        for funkce in self.seznamFunkci:
            if len(args) == 0:
                funkce()
            else:
                funkce(args)

class ObrazkovySprite(Sprite):
    def __init__(self, x, y , obrazek_cesta: str,*groups: Group) -> None:
        super().__init__(*groups)
        self.naKlik = Akce()
        self.x = x
        self.y = y
        self.image = pygame.image.load(obrazek_cesta)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False


    

pygame.init()

# Set up display dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Backamon")

sprites = Group()
rndSprite = ObrazkovySprite(50,50,"pomocnyMaterial\deskaLayout.png")
rndSprite.naKlik.pridejAkci(lambda x: print(x[1]))
rndSprite.naKlik.pridejAkci(lambda x: print(x))
sprites.add(rndSprite)



VybranyKamen = Kamen()
#Ukaž možnosti specifického kamene

#Pokud nemá kámen vybrané kameny ukáže všechny kamena nebo ukáže v BARU pokud tam nějakej je
running = True

vybranePolicko = None
clovekHrac = Hrac(Pozice(100,100))
hra = Hra(clovekHrac,Hrac(Pozice(100,200)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if hra.hracNaRade(clovekHrac):
                for sprite in sprites:
                    if sprite.rect.collidepoint(event.pos):
                            if sprite is Policko:
                               vybranePolicko = sprite
                      

    screen.fill((0, 0, 0))
    sprites.draw(screen)
    pygame.display.flip()

pygame.quit()