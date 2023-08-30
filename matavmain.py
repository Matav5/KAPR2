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
clovekHrac = Hrac( "red_front_side.png",vykreslovaci_group)
hra = Hra(clovekHrac,Hrac( "white_front_side.png",vykreslovaci_group), vykreslovaci_group)

'''
for policko in hra.herniPole:
    for policko_kamen in policko.kameny:
         vykreslovaci_group.add(policko_kamen)

for policko in hra.herniPole:
    vykreslovaci_group.add(policko)
'''

running = True
while running:
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hra.update(event)
            
    # Vykreslení pozadí
    screen.blit(background_image, (0, 0))


    pygame.display.flip()
 
    vykreslovaci_group.draw(background_image)

    clock.tick(60)

pygame.quit()

