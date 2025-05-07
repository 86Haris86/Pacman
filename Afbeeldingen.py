# Import
import pygame

#----------------------------------------------------------------------------------------------------------------------#

# Maze1 (niets)
pacman_imgs = [pygame.image.load("LEVEL 3/mond_dicht.png"), pygame.image.load("LEVEL 3/mond_open.png"), pygame.image.load("LEVEL 3/mond_half_open.png")]
pacman_imgs_op_schaal = [pygame.transform.scale(img, (30, 30)) for img in pacman_imgs]

#----------------------------------------------------------------------------------------------------------------------#

# Maze2 (Naïl)
    # weg
donkergroen = pygame.transform.scale(pygame.image.load("Voetbal_decor/donkergroen.png"), (30, 30))


    # veld
lichtgroen = pygame.transform.scale(pygame.image.load("Voetbal_decor/lichtgroen.png"), (30, 30))
corner_LB = pygame.transform.scale(pygame.image.load("Voetbal_decor/corner(LB).png"), (30, 30))
corner_LBOVEN = pygame.transform.scale(pygame.image.load("Voetbal_decor/corner(LBOVEN).png"), (30, 30))
corner_RB_copy = pygame.transform.scale(pygame.image.load("Voetbal_decor/corner(RB) copy.png"), (30, 30))
corner_RBOVEN_copy_2 = pygame.transform.scale(pygame.image.load("Voetbal_decor/corner(RBOVEN) copy 2.png"), (30, 30))
separatie_boven = pygame.transform.scale(pygame.image.load("Voetbal_decor/separatie(boven).png"), (30, 30))
separatie = pygame.transform.scale(pygame.image.load("Voetbal_decor/separatie.png"), (30, 30))
wite_lijn_L = pygame.transform.scale(pygame.image.load("Voetbal_decor/wite lijn(L).jpg"), (30, 30))
wite_lijn_R = pygame.transform.scale(pygame.image.load("Voetbal_decor/wite lijn(R).png"), (30, 30))

#----------------------------------------------------------------------------------------------------------------------#

# Maze3 (Haris)

#afbeeldingen
speed_img = pygame.transform.scale(pygame.image.load("LEVEL 3/auto_30x30.png"), (30, 30))
crocoo1 = pygame.transform.scale(pygame.image.load("LEVEL 3/crocooo_processed.png"), (30, 30))
etoue_30x30 = pygame.transform.scale(pygame.image.load("LEVEL 3/etoue_30x30.jpg"), (30, 30))
gier1 = pygame.transform.scale(pygame.image.load("LEVEL 3/gier.png"), (30, 30))
greenbleu_30x30 = pygame.transform.scale(pygame.image.load("LEVEL 3/greenbleu_30x30.jpg"), (30, 30))
hart1 = pygame.transform.scale(pygame.image.load("LEVEL 3/hart1.png"), (30, 30))
hippo1 = pygame.transform.scale(pygame.image.load("LEVEL 3/hippo_processed.png"), (30, 30))
leeuw1 = pygame.transform.scale(pygame.image.load("LEVEL 3/leeuw1.png"), (30, 30))
neushoorn1 = pygame.transform.scale(pygame.image.load("LEVEL 3/neushoorn1.png"), (30, 30))
olifant1 = pygame.transform.scale(pygame.image.load("LEVEL 3/olifant1.png"), (30, 30))
resized_tile_0_4 = pygame.transform.scale(pygame.image.load("LEVEL 3/resized_tile_0_4 (1).png"), (30, 30))
way_30x30 = pygame.transform.scale(pygame.image.load("LEVEL 3/way_30x30.jpeg"), (30, 30))
yellow_green_gradient = pygame.transform.scale(pygame.image.load("LEVEL 3/yellow_green_gradient.png"), (30, 30))


leeuw = "LEVEL 3/leeuw1.png"
crocoo = "LEVEL 3/crocooo_processed.png"
hippo = "LEVEL 3/hippo_processed.png"
olifant = "LEVEL 3/olifant1.png"
neushoorn = "LEVEL 3/neushoorn1.png"
gier = "LEVEL 3/gier.png"



#----------------------------------------------------------------------------------------------------------------------#