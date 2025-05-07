# Import and initialize the pygame library
import pygame



# Initialisatie
pygame.init()


# imports van andere files
from Afbeeldingen import pacman_imgs_op_schaal
from Setting import muurgrootte , gebruikte_maze, maze3 , startzone_tegel , eindzone_x ,eindzone_y
from Setting import leeuw_active , olifant_active , neushoorn_active , gier_active , croco_active , hippo_active , soort1 , soort2 , soort3 , soort4 , soort5 , soort6
from Setting import breedte, hoogte, screen, tijd, fps, font, deur_van_spoken, tekst_punten_x, tekst_punten_y, tekst_tijd_x, tekst_tijd_y
from Setting import ROOD , ZWART , WIT , GROEN , walls , items , items2 , toegelaten_posities_speler , toegelaten_posities_vijand , snelheids_object
from Setting import start_positie_x_speler1 , start_positie_y_speler1 , start_positie_x_soort1, start_positie_y_soort1 , start_positie_x_soort2, start_positie_y_soort2 , start_positie_x_soort3, start_positie_y_soort3
from Setting import start_positie_x_soort4, start_positie_y_soort4 , start_positie_x_soort5, start_positie_y_soort5, start_positie_x_soort6, start_positie_y_soort6
from Hulpfuncties import toon_levens
from Speler import Speler , radius_speler , snelheid_speler
from Vijand import Spook , snelheid_monster , snelheid_monster_2


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

# Spelers & Spoken aanmaken
speler = Speler(start_positie_x_speler1 , start_positie_y_speler1, screen, WIT, radius_speler, snelheid_speler , toegelaten_posities_speler, pacman_imgs_op_schaal)
leeuw = Spook(start_positie_x_soort1, start_positie_y_soort1 , screen, soort1, snelheid_monster, "pinky" , toegelaten_posities_vijand , leeuw_active )
olifant = Spook(start_positie_x_soort2, start_positie_y_soort2 , screen, soort2, snelheid_monster, "blinky" , toegelaten_posities_vijand , olifant_active )
neushoorn = Spook(start_positie_x_soort3, start_positie_y_soort3 , screen, soort3, snelheid_monster, "inky" , toegelaten_posities_vijand , neushoorn_active )
gier = Spook(start_positie_x_soort4, start_positie_y_soort4 , screen, soort4, snelheid_monster, "clyde" , toegelaten_posities_vijand , gier_active )
croco = Spook(start_positie_x_soort5, start_positie_y_soort5, screen,  soort5, snelheid_monster_2 , "blinky", toegelaten_posities_vijand , croco_active )
hippo = Spook(start_positie_x_soort6, start_positie_y_soort6, screen,  soort6, snelheid_monster_2, "blinky", toegelaten_posities_vijand , hippo_active )

list_of_objects = [speler, leeuw, olifant, neushoorn, gier , croco, hippo]
list_of_monsters = [leeuw, olifant, neushoorn, gier , croco, hippo]

# Game-loop
running = True
while running:
    tijd.tick(fps)
    screen.fill(ZWART)

    # Speler tekenen
    speler.draw()
    speler.patrol()
    speler.overdracht()
    # tegel waar de speler staat
    speler_tegel_x, speler_tegel_y = speler.x // muurgrootte, speler.y // muurgrootte
    speler_tegel = (speler_tegel_x, speler_tegel_y)
    # tekent de spoken en 'doet de spoken bewegen'
    for obj in list_of_monsters:
        obj.draw()
        obj.overdracht()
        obj.patrol(speler, olifant)

    # 1. Normale items pakken
    for item in items[:]:
        if item.botsing(speler):
            items.remove(item)
            speler.punten += item.punten()

    # 2. Speciale items pakken om eetmodus te starten
    for item in items2[:]:
        if item.botsing(speler):
            items2.remove(item)
            speler.start_eetmodus()

            # Zet alle spoken tijdelijk in "vlucht" modus
            for spook in list_of_monsters:
                spook.verander_type("vlucht")
                spook.removeposities(toegelaten_posities_vijand,deur_van_spoken)

    # 3. Spoken checken
    for spook in list_of_monsters:
        if speler.check_collision(spook):
            if speler.eetmodus_actief():
                speler.punten += speler.eetspook(spook)  # alleen eet als eetmodus actief
                spook.verander_type(spook.oorspronkelijk_type)  # Zet type terug
            else:
                #speler.levens -= 1
                speler.reset()
                for spooks in list_of_monsters:
                    spooks.reset()
                    spook.appendposities(toegelaten_posities_vijand, deur_van_spoken)
                pygame.time.delay(500)

    # 4. Check na botsing of eetmodus voorbij is
    if not speler.eetmodus_actief():
        for spook in list_of_monsters:
            spook.verander_type(spook.oorspronkelijk_type)  # Zet type terug
            spook.appendposities(toegelaten_posities_vijand, deur_van_spoken)
        speler.eetcombo = 0
    # teken het snelheidsobject als het nog bestaat
    if not snelheids_object.botsing(speler) :
        snelheids_object.draw()

    # Check of speler het snelheidsobject raakt , indien wel start het de snelheid en verwijder de object
    if snelheids_object and snelheids_object.botsing(speler):
        speler.activeer_snelheid()
        snelheids_object.delete()

    # Check of snelheidstimer verlopen is
    speler.update_snelheid()

    # controleer of speler trigger bereikt ( bv op tegel 15,9)
    speler_tegel_x , speler_tegel_y = speler.x // muurgrootte , speler.y // muurgrootte
    if gebruikte_maze == maze3 and speler.is_op_triggertegel([(24, 13), (24, 17)]):
        croco.zet_actief(True)
        hippo.zet_actief(True)

    # Score en timer tonen
    score_text = font.render(f"Score: {speler.punten}", True, WIT)
    screen.blit(score_text, (tekst_punten_x, tekst_punten_y))
    speler.toon_timer(screen, font, tekst_tijd_x, tekst_tijd_y, WIT)

    # Levens tonen
    toon_levens(screen, speler.levens)

    if speler.levens <= 0:
        font = pygame.font.SysFont(None, 75)
        tekst = font.render("Game Over", True, ROOD)
        screen.blit(tekst, (breedte // 2 - 150, hoogte // 2 - 40))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    alle_items_opgeraakt = len(items) == 0 and len(items2) == 0

    if alle_items_opgeraakt:
        pygame.draw.rect(screen, GROEN, (eindzone_x,eindzone_y, muurgrootte, muurgrootte))

    if alle_items_opgeraakt and speler_tegel == startzone_tegel:
        font = pygame.font.SysFont(None, 75)
        tekst = font.render("GEWONNEN!", True, (0, 255, 0))
        screen.blit(tekst, (breedte // 2 - 150, hoogte // 2 - 40))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Muren tekenen
    for wall in walls:
        wall.draw()

    # Items tekenen
    for item in items:
        item.draw()
    for item in items2:
        item.draw()

    # --> HIER score tonen
    score_text = font.render(f"Score: {speler.punten}", True, WIT)
    screen.blit(score_text, (tekst_punten_x , tekst_punten_y))
    speler.toon_timer(screen, font , tekst_tijd_x , tekst_tijd_y , WIT)

    pygame.display.flip()

pygame.quit()

#----------------------------------------------------------------------------------------------------------------------#
