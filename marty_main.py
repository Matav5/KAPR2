
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from jv_matav import Policko, Kamen, Hra, Hrac

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
        print("Jsem v ZmenStatus!")
        self.status = False
        for i in self.buttons:
            i.hide()
        menu.RollDice()

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
        print("Vytvořil jsem AIButton!")


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
        onClick=self.ZmenStatus
        ))
        print("Vytvořil jsem ProtiHracButton!")

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
        self.buttons.append(self.rollbutton)
        print("Vytvořil jsem hod kostkou!")

class InfoInGame:
    def __init__(self):
        self.textKotka = ""
        self.textHra = ""

    def InfoKostky(self, vstup):
        text = "KOSTKY: "
        for i in vstup:
            text += " | "+str(i)+ " | "
        self.textKostka = text

    def InfoHra(self, vstup):
        self.textHra = "Hrac: " + str(vstup)

    def ZobrazTextKostka(self, screen):
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.textKostka, True, (255, 255, 255))
        screen.blit(text_surface, (100, 50))

    def ZobrazTextHra(self, screen):
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.textHra, True, (0, 0, 0))
        screen.blit(text_surface, (100, 100))
#----------------------------------------------------------------------------
class GlowTahy:
    def __init__(self, image_pathUp, image_pathDown):
        self.imageUp = pygame.image.load(image_pathUp)
        self.imageDown = pygame.image.load(image_pathDown)
        self.rect1 = self.imageUp.get_rect()
        self.rect2 = self.imageDown.get_rect()
        self.rect3 = self.imageUp.get_rect()
        self.pole = []
        self.rect_to_print = []
        self.printed_rect = []

    def NajdiPole(self, hra):
        self.pole.clear()
        self.rect_to_print.clear()
#pokud je policko none, tak chci zvyraznit bar
        if hra.kliknutePole != None:
            print("Vybrane pole existuje!")

            print(f"Vybrane policko {hra.kliknutePole}")
            tahy = hra.vypisTah(hra.dvojKostka.seznamHodnot, hra.kliknutePole.souradnice)
            print(f"NAŠLÉ TAHY PRO POLE: {tahy}")

            for pole in tahy:
                if pole.policko.souradnice == -1 or pole.policko.souradnice == 24:
                    pos_domecek = pole.kamen.hrac.domecek.pozice

                    new_rect = self.rect3.copy()
                    new_rect.centerx = pos_domecek.x  # Nastavte nový střed X
                    new_rect.centery = pos_domecek.y  # Nastavte nový střed Y
                    self.rect_to_print.append((self.imageUp, new_rect))
                    continue

                pole = pole.policko.pozice
                print(pole)
                #print(f"NENÍ NONE: {pole}")

                if pole.y > 500:
                    new_rect = self.rect1.copy()
                    new_rect.centerx = pole.x  # Nastavte nový střed X
                    new_rect.centery = pole.y  # Nastavte nový střed Y
                    self.rect_to_print.append((self.imageUp, new_rect))

                else:
                    new_rect = self.rect2.copy()
                    new_rect.centerx = pole.x  # Nastavte nový střed X
                    new_rect.centery = pole.y  # Nastavte nový střed Y
                    self.rect_to_print.append((self.imageDown, new_rect))

                self.pole.append(pole)

        else:
            tahy = hra.vypisTahyPolicek(hra.dvojKostka.seznamHodnot)

            for pole in tahy:
                #print(f"JE NONE: {pole}")
                pole = hra.herniPole[pole.kamen.souradnice].pozice
                #print(f"SOURADNICE: ({pole.x},{pole.y}) souradnice")
                if pole.y > 500:
                    new_rect = self.rect1.copy()
                    new_rect.centerx = pole.x  # Nastavte nový střed X
                    new_rect.centery = pole.y  # Nastavte nový střed Y
                    self.rect_to_print.append((self.imageUp, new_rect))

                else:
                    new_rect = self.rect2.copy()
                    new_rect.centerx = pole.x  # Nastavte nový střed X
                    new_rect.centery = pole.y  # Nastavte nový střed Y
                    self.rect_to_print.append((self.imageDown, new_rect))

                self.pole.append(pole)

        return self.pole, self.rect_to_print

    def ZobrazPole(self, surface):
        for rec in self.rect_to_print:
            x = surface.blit(rec[0], rec[1])
            self.printed_rect.append(x)
            lambda: x

info = InfoInGame()
info.InfoHra(hra.aktualniHrac)
glow = GlowTahy('glow_tahy_up.png', 'glow_tahy_down.png')
menu = Menu()

print(f"SEZNAM TLAČÍTEK: {menu.buttons}")
#----------------------------------------------------------------------------

for policko in hra.herniPole:
    for policko_kamen in policko.kameny:
         vykreslovaci_group.add(policko_kamen)

for policko in hra.herniPole:
    vykreslovaci_group.add(policko)

glow.NajdiPole(hra)

#----------------------------------------------------------------------------
running = True

while running:

    for event in pygame.event.get():
        glow.NajdiPole(hra)
        for button in menu.buttons:
            button.listen(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            hra.update(event)

    if menu.status:
        screen.blit(menu_image, (0, 0))

        for button in menu.buttons:
            button.draw()

    else:
        screen.blit(background_image, (0, 0))

    if not menu.status:
        menu.rollbutton.draw()
        glow.ZobrazPole(screen)

        info.InfoKostky(hra.dvojKostka.seznamHodnot)
        info.InfoHra(hra.aktualniHrac)

        info.ZobrazTextKostka(screen)
        info.ZobrazTextHra(screen)

        try:
            vykreslovaci_group.draw(screen)
        except:
            pass

    pygame.display.flip()
    clock.tick(60)
    pygame_widgets.update(event)

pygame.quit()
