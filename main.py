import pygame
from pygame.sprite import  Sprite, Group
from matav import Policko, Kamen, Hra, Hrac, Pozice

pygame.init()
clock = pygame.time.Clock()

# Nastavení rozměrů okna
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kaminky")

background_image = pygame.image.load("hraci_plocha_komplet.jpg")  # Nahrání obrázku pozadí
background_image = pygame.transform.scale(background_image, (width, height))  # Přizpůsobení rozměrů okna

#----------------------------------------------------------------------
#SPRITE CLASS
'''class GUIKamen(Kamen,pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player, *groups :Group):
        super().__init__(0,player)
        pygame.sprite.Sprite.__init__(self,groups)

        self.image = pygame.image.load("white_front_side.png") #image dat do hrace
      #  self.image = player.image
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]

class GUIPolicko(Policko,pygame.sprite.Sprite):
    def __init__(self, souradnice, x,y, *groups :Group):
        super().__init__(souradnice, x,y)
        pygame.sprite.Sprite.__init__(self,groups)
'''
#----------------------------------------------------------------------

vykreslovaci_group =  pygame.sprite.Group()

vybranePolicko = None
clovekHrac = Hrac(Pozice(100,100), "white_front_side.png")
hra = Hra(clovekHrac,Hrac(Pozice(100,200), "white_front_side.png"))


for policko in hra.herniPole:
    for policko_kamen in policko.kameny:
         vykreslovaci_group.add(policko_kamen)

for policko in hra.herniPole:
    vykreslovaci_group.add(policko)


running = True
while running:
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hra.hracNaRade(clovekHrac):
                for sprite in vykreslovaci_group:
                    if sprite.rect.collidepoint(event.pos):
                        if type(sprite) is Policko:
                         '''   if vybranePolicko != sprite:
                                if vybranePolicko != None:
                                    odebranyKamen = vybranePolicko.odeberKamen()
                                    if odebranyKamen != None:
                                        sprite.pridejKamen(odebranyKamen)
                                        print(vybranePolicko.souradnice)
                                        vybranePolicko = None
                                    else:
                                        print(vybranePolicko.souradnice)
                                else:
                                    vybranePolicko = sprite
                                    '''
                            print("Poličko")
                        if type(sprite) is Kamen:
                            print("Kamen")
    # Vykreslení pozadí
    screen.blit(background_image, (0, 0))


    pygame.display.flip()
    try:
        vykreslovaci_group.draw(background_image)
    except:
        pass
    clock.tick(60)

pygame.quit()

