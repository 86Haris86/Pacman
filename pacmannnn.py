# Import and initialize the pygame library
import pygame
import heapq

# Initialisatie
pygame.init()

# Scherminstellingen
breedte = int(870)
hoogte = int(570)
screen = pygame.display.set_mode([breedte, hoogte])
#screen = pygame.display.set_mode([breedte, hoogte], pygame.FULLSCREEN)


# Kleuren
WIT = (255, 255, 255)
BLAUW = (0, 0, 128)
BLACK = (0, 0, 0)
ROOD = (255, 0, 0)
GROEN = (0, 255, 0)
GEEL = (255, 255, 0)
ZWART = (0, 0, 0)

# Tijd
time = pygame.time.Clock()
fps = 30

# Grootte van muur en rand
muurgrootte = 30
balgrootte = 5
balgrootte1 = 9

# Overdrachtszones
zone1 = (45, 225)
zone2 = (825, 465)

#zone1 = (45, 225)
#zone1 = (45, 225)

#zone1 = (45, 225)
#zone1 = (45, 225)

#activatie van croco en hippo (Flags)
croco_active = False
hippo_active = False




# Menu tonen
def toon_menu():
    achtergrond = pygame.image.load("achtergrond_savanne.png")
    achtergrond = pygame.transform.scale(achtergrond, (breedte, hoogte))
    font = pygame.font.SysFont(None, 75)
    knop_rect = pygame.Rect(breedte // 2 - 100, hoogte // 2 - 50, 200, 100)

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if knop_rect.collidepoint(event.pos):
                    menu_running = False

        screen.blit(achtergrond, (0, 0))
        pygame.draw.rect(screen, GROEN, knop_rect)
        tekst = font.render("Start", True, ZWART)
        screen.blit(tekst, (knop_rect.x + 40, knop_rect.y + 25))

        pygame.display.flip()

toon_menu()

# Maze laden
def maze_van_bestand(bestand):
    document = []
    file = open(bestand, 'r')
    for lijn in file:
        lijn = lijn.strip().split()
        lijn = [int(cijfer) for cijfer in lijn]
        document.append(lijn)
    file.close()
    return document

maze = maze_van_bestand("maze3.txt")

# Muur Klasse
class Muur:
    def __init__(self, x, y, size, kleur=None, afbeelding=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.kleur = kleur
        self.afbeelding = afbeelding

    def draw(self, surface):
        if self.afbeelding:
            surface.blit(self.afbeelding, self.rect)
        else:
            pygame.draw.rect(surface, self.kleur, self.rect)

# Object Klassen
class Object1:
    def __init__(self,x, y, afmeting, kleur, scherm, type, afbeelding=None):
        self.x = x
        self.y = y
        self.afmeting = afmeting
        self.kleur = kleur
        self.scherm = scherm
        self.type = type
        self.center = (x + muurgrootte // 2, y + muurgrootte // 2)
        self.radius = afmeting // 2
        self.afbeelding = afbeelding

    def draw(self):
        if self.afbeelding:
            rect = self.afbeelding.get_rect(topleft=(self.x, self.y))
            self.scherm.blit(self.afbeelding, rect)
        else:
            pygame.draw.circle(self.scherm, self.kleur, self.center, self.radius)

    def botsing(self, speler):
        spelerx1 = speler.x - speler.radius
        spelerx2 = speler.x + speler.radius
        spelery1 = speler.y - speler.radius
        spelery2 = speler.y + speler.radius
        x1 = self.x
        x2 = self.x + self.afmeting
        y1 = self.y
        y2 = self.y + self.afmeting
        if spelerx2 > x1 and spelerx1 < x2 and spelery2 > y1 and spelery1 < y2:
            return True
        return False

class Object2(Object1):
    pass


#bush = pygame.transform.scale(pygame.image.load("struik/bush.png"), (30, 30))

#afbeeldingen
img_wall0 = pygame.transform.scale(pygame.image.load("LEVEL 3/way_30x30.jpeg"), (30, 30))
greenbleu_30x30 = pygame.transform.scale(pygame.image.load("LEVEL 3/greenbleu_30x30.jpg"), (30, 30))
etoue_30x30 = pygame.transform.scale(pygame.image.load("LEVEL 3/etoue_30x30.jpg"), (30, 30))
yellow_green_gradient = pygame.transform.scale(pygame.image.load("LEVEL 3/yellow_green_gradient.png"), (30, 30))
resized_tile_0_4 = pygame.transform.scale(pygame.image.load("LEVEL 3/resized_tile_0_4 (1).png"), (30, 30))
speed_img = pygame.transform.scale(pygame.image.load("LEVEL 3/auto_30x30.png"), (30, 30))
pacman_imgs = [
    pygame.image.load("LEVEL 3/mond_dicht.png"),
    pygame.image.load("LEVEL 3/mond_open.png"),
    pygame.image.load("LEVEL 3/mond_half_open.png")
]
# Schaal de afbeeldingen eventueel naar je gewenste grootte
pacman_imgs = [pygame.transform.scale(img, (30, 30)) for img in pacman_imgs]


# Walls en Items vullen
walls = []
items = []

for row_index, row in enumerate(maze):
    for col_index, tile in enumerate(row):
        x = col_index * muurgrootte
        y = row_index * muurgrootte
        if tile == 0:
            items.append(Object1(x, y, balgrootte, WIT, screen, type=1))
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_wall0))
        elif tile == 1:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_4))
        elif tile == 2:
            walls.append(Muur(x, y, muurgrootte, kleur=ROOD))
        elif tile == 3:
            walls.append(Muur(x, y, muurgrootte, kleur=GEEL))
        elif tile == 4:
            walls.append(Muur(x, y, muurgrootte, kleur=GROEN))
        elif tile == 5:
            items.append(Object2(x, y, balgrootte1, WIT, screen, type=2))
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_wall0))
        elif tile == 6:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_4))
        elif tile == 7:
            walls.append(Muur(x, y, muurgrootte, afbeelding=yellow_green_gradient))
        elif tile == 8:
            walls.append(Muur(x, y, muurgrootte, afbeelding=etoue_30x30))
        elif tile == 9:
            walls.append(Muur(x, y, muurgrootte, afbeelding=greenbleu_30x30))
        elif tile == 10:
            walls.append(Muur(x, y, muurgrootte, afbeelding=etoue_30x30))




class MazeChecker:
    def __init__(self, maze, tile_size):
        self.maze = maze
        self.tile_size = tile_size

    def is_valid(self, x, y):
        kol = int(x) // self.tile_size
        rij = int(y) // self.tile_size
        if 0 <= rij < len(self.maze) and 0 <= kol < len(self.maze[0]):
            return self.maze[rij][kol] in (0, 4, 5, 6, 9, 10)
        return False

maze_checker = MazeChecker(maze, muurgrootte)

import random

# Zoek alle lege tegels (waarde 0) in het doolhof
lege_plekken = [(j * muurgrootte, i * muurgrootte) for i, rij in enumerate(maze) for j, waarde in enumerate(rij) if waarde == 0]

# Kies willekeurig een positie voor het snelheidsobject
x_snelheid, y_snelheid = random.choice(lege_plekken)

# Maak het snelheidsobject aan (je kan hier een afbeelding toevoegen later)
snelheids_object = snelheids_object = Object1(x_snelheid, y_snelheid, muurgrootte, WIT, screen, type=99, afbeelding=speed_img)
snelheids_object.afbeelding = speed_img


# A* algoritme om kortste pad te berekenen tussen start en doel

def a_star(maze, start, goal, tile_size):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    rows, cols = len(maze), len(maze[0])
    start_tile = (start[1] // tile_size, start[0] // tile_size)
    goal_tile = (goal[1] // tile_size, goal[0] // tile_size)

    frontier = [(0, start_tile)]
    came_from = {start_tile: None}
    cost_so_far = {start_tile: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal_tile:
            break

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dy, current[1] + dx
            if 0 <= nx < rows and 0 <= ny < cols and maze[int(nx)][int(ny)] in (0, 2, 4, 9):
                next_tile = (int(nx), int(ny))
                new_cost = cost_so_far[current] + 1
                if next_tile not in cost_so_far or new_cost < cost_so_far[next_tile]:
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + heuristic(goal_tile, next_tile)
                    heapq.heappush(frontier, (priority, next_tile))
                    came_from[next_tile] = current

    path = []
    current = goal_tile
    while current != start_tile:
        if current in came_from:
            path.append((current[1] * tile_size + tile_size//2, current[0] * tile_size + tile_size//2))
            current = came_from[current]
        else:
            return []
    path.reverse()
    return path

# Klasse die de speler representeert en beweging/leven/overdracht regelt
class Speler:
    def __init__(self, x, y, kleur, radius, snelheid):
        self.x, self.y = x, y
        self.kleur = kleur
        self.radius = radius
        self.snelheid = snelheid
        self.initial_state = (x, y)
        self.levens = 3
        self.animatie_index = 0
        self.animatie_teller = 0
        self.richting = "rechts"  # standaard richting

    def draw(self, screen):
        img = pacman_imgs[self.animatie_index]

        # Afbeelding roteren op basis van richting
        if self.richting == "rechts":
            rotated = img
        elif self.richting == "links":
            rotated = pygame.transform.flip(img, True, False)
        #elif self.richting == "omhoog":
            #rotated = pygame.transform.rotate(img, 180)
        elif self.richting == "omhoog":
            rotated = pygame.transform.rotate(img, 90)
        elif self.richting == "omlaag":
            rotated = pygame.transform.rotate(img, -90)
        #else:
         #   rotated = img  # fallback

        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)

    def update_animatie(self):
        self.animatie_teller += 1
        if self.animatie_teller % 10 == 0:
            self.animatie_index = (self.animatie_index + 1) % len(pacman_imgs)

    def move(self, dx, dy):
        stappen = int(max(abs(dx), abs(dy)))
        if stappen == 0:
            return

        # Richting bepalen vóór beweging
        if dx > 0:
            self.richting = "rechts"
        elif dx < 0:
            self.richting = "links"
        elif dy < 0:
            self.richting = "omhoog"
        elif dy > 0:
            self.richting = "omlaag"

        stap_dx = dx / stappen
        stap_dy = dy / stappen

        for _ in range(stappen):
            nieuw_x = self.x + stap_dx
            nieuw_y = self.y + stap_dy

            hoeken = [
                (nieuw_x + self.radius, nieuw_y + self.radius),
                (nieuw_x + self.radius, nieuw_y - self.radius),
                (nieuw_x - self.radius, nieuw_y + self.radius),
                (nieuw_x - self.radius, nieuw_y - self.radius)
            ]

            if all(maze_checker.is_valid(x, y) for x, y in hoeken):
                self.x = nieuw_x
                self.y = nieuw_y
                self.update_animatie()
            else:
                return

    def patrol(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:  self.move(0, self.snelheid)
        if keys[pygame.K_UP]:    self.move(0, -self.snelheid)
        if keys[pygame.K_LEFT]:  self.move(-self.snelheid, 0)
        if keys[pygame.K_RIGHT]: self.move(self.snelheid, 0)

    def reset(self):
        self.x, self.y = self.initial_state

    def overdracht(self):
        if (self.x, self.y) == zone1:
            self.x, self.y = zone2
        elif (self.x, self.y) == zone2:
            self.x, self.y = zone1



# Klasse voor vijanden (spoken), met AI gedrag per type
class Spook:
    def __init__(self, x, y, afbeelding_pad, snelheid, type):
        self.x, self.y = x, y
        self.snelheid = snelheid
        self.afbeelding = pygame.image.load(afbeelding_pad)
        self.afbeelding = pygame.transform.scale(self.afbeelding, (37, 37))
        self.rect = self.afbeelding.get_rect(center=(x, y))
        self.initial_state = (x, y)
        self.pad = []
        self.doel_index = 0
        self.type = type

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.afbeelding, self.rect)

    def volg_pad(self):
        if self.doel_index < len(self.pad):
            doel_x, doel_y = self.pad[self.doel_index]
            dx = doel_x - self.x
            dy = doel_y - self.y
            afstand = (dx**2 + dy**2) ** 0.5
            if afstand < self.snelheid:
                self.x, self.y = doel_x, doel_y
                self.doel_index += 1
            else:
                self.x += self.snelheid * dx / afstand
                self.y += self.snelheid * dy / afstand

    def patrol(self, speler, extra_speler=None):
        if self.doel_index >= len(self.pad):
            if self.type == "blinky":
                target = (speler.x, speler.y)
            elif self.type == "pinky":
                dx, dy = 0, 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]: dy = -4 * muurgrootte
                elif keys[pygame.K_DOWN]: dy = 4 * muurgrootte
                elif keys[pygame.K_LEFT]: dx = -4 * muurgrootte
                elif keys[pygame.K_RIGHT]: dx = 4 * muurgrootte
                target = (speler.x + dx, speler.y + dy)
            elif self.type == "inky":
                dx, dy = 0, 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]: dy = -2 * muurgrootte
                elif keys[pygame.K_DOWN]: dy = 2 * muurgrootte
                elif keys[pygame.K_LEFT]: dx = -2 * muurgrootte
                elif keys[pygame.K_RIGHT]: dx = 2 * muurgrootte
                projected = (speler.x + dx, speler.y + dy)
                if extra_speler:
                    vx = projected[0] - extra_speler.x
                    vy = projected[1] - extra_speler.y
                    target = (extra_speler.x + 2 * vx, extra_speler.y + 2 * vy)
                else:
                    target = projected
            elif self.type == "clyde":
                afstand = ((self.x - speler.x)**2 + (self.y - speler.y)**2)**0.5
                if afstand > 160:
                    target = (speler.x, speler.y)
                else:
                    target = (1 * muurgrootte, 17 * muurgrootte)
            else:
                target = (speler.x, speler.y)
            self.pad = a_star(maze, (self.x, self.y), target, muurgrootte)
            self.doel_index = 0
        self.volg_pad()

    def reset(self):
        self.x, self.y = self.initial_state
        self.pad = []  # ❗ Leeg pad bij reset
        self.doel_index = 0  # ❗ Zorg dat hij bij volgende patrol direct een nieuw pad berekent

    def overdracht(self):

        if (self.x, self.y) == zone1:
            self.x, self.y = zone2
        elif (self.x, self.y) == zone2:
            self.x, self.y = zone1



# Checkt of speler en spook: leeuwen etc voila botsen met elkaar
def check_collision(speler, spook):
    speler_rect = pygame.Rect(speler.x - speler.radius, speler.y + speler.radius , speler.radius-5, speler.radius+5)
    return speler_rect.colliderect(spook.rect)


# Teken hartjes linksboven misschien later voor elk niveau iets anders
def toon_levens(screen, levens):
    hart_afbeelding = pygame.image.load("LEVEL 3/hart1.png")
    hart_afbeelding = pygame.transform.scale(hart_afbeelding, (25, 25))
    for i in range(levens):
        screen.blit(hart_afbeelding, (10 + i * 35, 10))

def herstart_spel(speler, spoken):
    speler.levens -= 1
    speler.reset()
    for spook in spoken:
        spook.reset()
        spook.pad = []         # 👈 Leeg het oude pad
        spook.doel_index = 0   # 👈 Zet index terug op 0 zodat hij direct herberekent
    pygame.time.delay(1000)



# Spelers & Spoken aanmaken
speler = Speler(435, 285, WIT, 14, 5)
leeuw = Spook(1 * muurgrootte + 15, 1 * muurgrootte + 15, "LEVEL 3/leeuw1.png", 3,"pinky")
olifant = Spook(27 * muurgrootte + 15, 1 * muurgrootte + 15 , "LEVEL 3/olifant1.png", 3, "blinky")
neushoorn = Spook(1 * muurgrootte + 15, 10 * muurgrootte + 15, "LEVEL 3/neushoorn1.png", 3, "inky")
gier = Spook(27 * muurgrootte + 15, 10 * muurgrootte + 15, "LEVEL 3/gier.png", 3, "clyde")
croco = Spook(27 * muurgrootte + 15, 13 * muurgrootte + 15, "LEVEL 3/crocooo_processed.png", 6.001, "blinky")
hippo = Spook(27 * muurgrootte + 15, 17 * muurgrootte + 15, "LEVEL 3/hippo_processed.png", 6.001, "blinky")

list_of_objects = [speler, leeuw, olifant, neushoorn, gier, croco, hippo]

# Game-loop
running = True
while running:
    time.tick(fps)
    screen.fill(ZWART)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    for wall in walls:
        wall.draw(screen)

    for item in items:
        item.draw()

    for obj in list_of_objects:
        obj.draw(screen)
        if isinstance(obj, Spook):
            obj.patrol(speler, olifant)
        else:
            obj.patrol()
        obj.overdracht()

    for item in items[:]:
        if item.botsing(speler):
            items.remove(item)

    if any(check_collision(speler, spook) for spook in [leeuw, olifant, neushoorn, gier]):
        speler.levens -= 1
        speler.reset()
        for spook in [leeuw, olifant, neushoorn, gier]:
            spook.reset()
        pygame.time.delay(500)

    toon_levens(screen, speler.levens)

    if speler.levens <= 0:
        font = pygame.font.SysFont(None, 75)
        tekst = font.render("Game Over", True, ROOD)
        screen.blit(tekst, (breedte // 2 - 150, hoogte // 2 - 40))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()