# Import
import pygame

#from Setting import muurgrootte , refactor
muurgrootte = 30
refactor = 1

#----------------------------------------------------------------------------------------------------------------------#

# Voorstelling van het plan
class Plan:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# specifiek over de muren van de plan
class Muur(Plan):
    def __init__(self, x, y, scherm, afmeting, kleur= None, afbeelding=None):
        super().__init__(x, y)
        self.scherm = scherm
        self.afmeting = afmeting
        self.kleur = kleur
        self.afbeelding = afbeelding

        self.rect = pygame.Rect(x, y, afmeting, afmeting)

    def draw(self):
        if self.afbeelding:
            self.scherm.blit(self.afbeelding, self.rect)
        else:
            pygame.draw.rect(self.scherm, self.kleur, self.rect)

#----------------------------------------------------------------------------------------------------------------------#

# Basis Objectklasse
# BasisObject
class BasisObject(Plan):
    def __init__(self, x, y, scherm, afmeting, kleur=None, afbeelding=None):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.scherm = scherm
        self.afmeting = int(afmeting)
        self.kleur = kleur
        self.afbeelding = afbeelding

        self.straal = self.afmeting // 2
        self.center = (x + muurgrootte // 2, y + muurgrootte // 2)
        self.centerbalx = self.center[0]
        self.centerbaly = self.center[1]

        self.aanwezig = True

    def draw(self):
        if not self.aanwezig:
            return
        else :
            if self.afbeelding:
                rect = self.afbeelding.get_rect(topleft=(self.x, self.y))
                self.scherm.blit(self.afbeelding, rect)
            else:
                pygame.draw.circle(self.scherm, self.kleur, self.center, self.straal)

    def botsing(self, personage):
        # Speler rechthoek (of ander bewegend object)
        spelerx1 = personage.x - personage.straal
        spelerx2 = personage.x + personage.straal
        spelery1 = personage.y - personage.straal
        spelery2 = personage.y + personage.straal

        # Object rechthoek
        x1 = self.centerbalx - self.straal
        x2 = self.centerbalx + self.straal
        y1 = self.centerbaly - self.straal
        y2 = self.centerbaly + self.straal

        return spelerx2 > x1 and spelerx1 < x2 and spelery2 > y1 and spelery1 < y2

    def punten(self):
        return 0  # Default, te overschrijven

    def aanwezig(self):
        self.aanwezig = True
        return self.aanwezig

    def delete(self):
        self.aanwezig = False
        return self.aanwezig

#----------------------------------------------------------------------------------------------------------------------#

# Object 1
class Object1(BasisObject):
    def punten(self):
        return 2

# Object 2
class Object2(BasisObject):
    def punten(self):
        return 10

# Object 3
class Snelheidsobject(BasisObject):
    def punten(self):
        return 10  # Geeft 10 punten bij het oppakken

    def aanwezig(self):
        self.aanwezig =  True

    def delete(self):
        self.aanwezig = False

