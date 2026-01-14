import pygame
import sys # Ajouté pour quitter proprement
import pyscroll
import pytmx
from Games.map.importmap import GameMap
from Games.entity.main_character.player import Player # Ton import

# Initialisation de Pygame
pygame.init()

# --- CONFIGURATION ECRAN ---
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Ashes Of Humanity")

# --- INITIALISATION OBJETS ---
gamemap = GameMap(screen_size)
clock = pygame.time.Clock()

# --- CREATION DU JOUEUR ET DU GROUPE ---
# Note : Ces lignes doivent être collées au bord gauche (pas d'espace au début)
print("Création du joueur...") # Debug : on vérifie que cette ligne s'exécute
player = Player(14192, 13349) #coordonné du spawn du joueur
player.walls = gamemap.walls
gamemap.group.add(player)
print("Joueur créé et ajouté au groupe !") # Debug
print(player.image.get_size())

running = True

# --- BOUCLE DU JEU ---
while running:
    clock.tick(60) # 60 FPS
    
    # 1. Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Mise à jour (Update)
    gamemap.group.update()


    # 3. Dessin (Draw)
    screen.fill((0, 0, 0)) # Fond noir pour nettoyer l'écran
    gamemap.group.center(player.rect.center)
    gamemap.render(screen, player.rect.center) #la camera suit le joueur
    gamemap.group.draw(screen)
    
    # D'abord la map (fond)
    
    # Ensuite le joueur (par dessus)

    # Rafraichissement final
    pygame.display.flip()

# Fin du programme
pygame.quit()
sys.exit()