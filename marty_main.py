
import pygame
from pygame_widgets.button import Button
from matav import Policko, Kamen, Hra, Hrac, Pozice

pygame.init()
clock = pygame.time.Clock()

width, height = 1920, 1080

class Menu():
    def __init__(self):
        self.status = True
        self.game_mode = None

    def ZmenStatus(self):
        self.status = False
        print("Button pressed!")
        self.zacnihru.hide()

    def AIButton(self):
        self.zacnihru = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        (width-600)/2,  # X-coordinate of top left corner
        (height-100)/2,  # Y-coordinate of top left corner
        600,  # Width
        100,  # Height

        # Optional Parameters
        text='Režim proti počítači',  # Text to display
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(255, 27, 27),  # Colour of button when not being interacted with
        hoverColour=(150, 0, 0),  # Colour of button when being hovered over
        pressedColour=(233, 200, 20),  # Colour of button when being clicked
        radius=20,  # Radius of border corners (leave empty for not curved)
        onClick=self.ZmenStatus
        )

    def ProtiHraciButton(self):
        self.zacnihru = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        (width-600)/2,  # X-coordinate of top left corner
        (height-100)/2 + 200,  # Y-coordinate of top left corner
        600,  # Width
        100,  # Height

        # Optional Parameters
        text='Režim proti hráči',  # Text to display
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(255, 27, 27),  # Colour of button when not being interacted with
        hoverColour=(150, 0, 0),  # Colour of button when being hovered over
        pressedColour=(233, 200, 20),  # Colour of button when being clicked
        radius=20,  # Radius of border corners (leave empty for not curved)
        onClick=self.ZmenStatus
        )

# Nastavení rozměrů okna
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kaminky")

background_image = pygame.image.load("hraci_plocha_komplet.jpg")  # Nahrání obrázku pozadí
background_image = pygame.transform.scale(background_image, (width, height))  # Přizpůsobení rozměrů okna

menu_image = pygame.image.load("menu_background.png")
menu_image = pygame.transform.scale(menu_image, (width, height))


vykreslovaci_group =  pygame.sprite.Group()
vybranePolicko = None
clovekHrac = Hrac(Pozice(100,100), "white_front_side.png")
hra = Hra(clovekHrac,Hrac(Pozice(100,200), "red_front_side.png"))
menu = Menu()

for policko in hra.herniPole:
    for policko_kamen in policko.kameny:
         vykreslovaci_group.add(policko_kamen)

for policko in hra.herniPole:
    vykreslovaci_group.add(policko)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hra.hracNaRade(clovekHrac):
                for sprite in vykreslovaci_group:
                    if sprite.rect.collidepoint(event.pos):
                        if type(sprite) is Policko:
                            if vybranePolicko != sprite:
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


                            print("Poličko")
                        if type(sprite) is Kamen:
                            print("Kamen")

    # Vykreslení pozadí
    if menu.status:
        screen.blit(menu_image, (0, 0))
        menu.AIButton()
        menu.ProtiHraciButton()

        pygame.update(event)

    else:
        screen.blit(background_image, (0, 0))

        try:
            vykreslovaci_group.draw(screen)
        except:
            pass

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

