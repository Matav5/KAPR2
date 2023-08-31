
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from matav import Policko, Kamen, Hra, Hrac, Pozice

pygame.init()
clock = pygame.time.Clock()

width, height = 1920, 1080

# Nastavení rozměrů okna
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kaminky")

background_image = pygame.image.load("hraci_plocha_komplet.jpg")  # Nahrání obrázku pozadí
background_image = pygame.transform.scale(background_image, (width, height))  # Přizpůsobení rozměrů okna

menu_image = pygame.image.load("menu_background.png")
menu_image = pygame.transform.scale(menu_image, (width, height))


vykreslovaci_group =  pygame.sprite.Group()
vybranePolicko = None

clovekHrac = Hrac( "red_front_side.png",vykreslovaci_group)
hra = Hra(clovekHrac,Hrac( "white_front_side.png",vykreslovaci_group), vykreslovaci_group)

class Menu:
    def __init__(self):
        self.status = True
        self.game_mode = None
        self.buttons = []
        self.aibutton = self.AIButton()
        self.playerbutton = self.ProtiHraciButton()
        self.rollbutton = None

    def ZmenStatus(self):
        self.status = False

        for i in self.buttons:
            i.hide()

    def AIButton(self):
        self.buttons.append(Button(
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
        ))
        print("Jsem AIButton!")


    def ProtiHraciButton(self):
        self.buttons.append(Button(
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
        onClick= self.ZmenStatus
        ))
        print("Jsem ProtiHracButton!")

    def RollDice(self):
        self.rollbutton = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        (width-600)/2,  # X-coordinate of top left corner
        50,  # Y-coordinate of top left corner
        600,  # Width
        50,  # Height

        # Optional Parameters
        text='Hoď kostkou',  # Text to display
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(255, 27, 27),  # Colour of button when not being interacted with
        hoverColour=(150, 0, 0),  # Colour of button when being hovered over
        pressedColour=(233, 200, 20),  # Colour of button when being clicked
        radius=20,  # Radius of border corners (leave empty for not curved)
        onClick=hra.dvojKostka.hod
        )

        self.ZmenStatus()
        self.buttons.append(self.rollbutton)

        print("Zmackl jsem kostky!!")

class InfoInGame:
    def __init__(self):
        self.text = ""
    def InfoKostky(self, vstup):
        self.text = vstup
    def InfoHra(self, vstup):
        self.text = vstup
    def ZobrazText(self, screen):
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (100, 50))

#----------------------------------------------------------------------------
class GlowTahy:
    def __init__(self):
        self.image = None
        self.pole = []

    def NajdiPole(self, hra, kostky):
        tahy = set(hra.vypisTahyPolicek(kostky)) #pryč duplicity
        for index, pole in tahy:
            print(pole.pozice)
            self.pole.append(pole.pozice)

        self.VyznacPole(self.pole)
        return self.pole
    def VyznacPole(self, pole: list):
        for g_pole in hra.herniPole:
            print(g_pole.pozice)
            for i in pole:
                print(i)
                if g_pole.pozice == i: #průnik tak budu higlightovat
                    pass
                    #tak highlight

menu = Menu()
info = InfoInGame()
info.InfoKostky("Čau")

glow = GlowTahy()
glow.NajdiPole(hra, [6, 6, 6, 6])

menu = Menu()
info = InfoInGame()
info.InfoKostky("Čau")
#----------------------------------------------------------------------------

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
                menu.RollDice()
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

    if menu.status:
        screen.blit(menu_image, (0, 0))

        for button in menu.buttons:
            button.listen(event)
            button.draw()

    else:
        screen.blit(background_image, (0, 0))

        try:
            vykreslovaci_group.draw(screen)
        except:
            pass

    # Vykreslení tlačítka pro hod kostkou
    if not menu.status:
        menu.rollbutton.listen(event)
        menu.rollbutton.draw()

        info.ZobrazText(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

