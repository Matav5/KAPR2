import pygame

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
class Kamen(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player):
        super().__init__()

        #self.image = pygame.image.load("white_front_side.png") #image dat do hrace
        #self.image = player.image
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]

kamen = Kamen(345,200)
kamen_group = pygame.sprite.Group()
kamen_group.add(kamen)
#----------------------------------------------------------------------


running = True
while running:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    # Vykreslení pozadí
    screen.blit(background_image, (0, 0))


    pygame.display.flip()
    kamen_group.draw(background_image)
    clock.tick(60)

pygame.quit()

