import pygame
import sys # Ajouté pour quitter proprement
from games.map.importmap import GameMap
from HashesOfHumanitie.games.entity.main_character.player import Player # Ton import

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
player = Player(400, 300)
player_group = pygame.sprite.Group()
player_group.add(player)
print("Joueur créé et ajouté au groupe !") # Debug

running = True

# --- BOUCLE DU JEU ---
while running:
    clock.tick(60) # 60 FPS
    
    # 1. Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Mise à jour (Update)
    player_group.update() # Le joueur calcule ses mouvements
    
    # 3. Dessin (Draw)
    screen.fill((0, 0, 0)) # Fond noir pour nettoyer l'écran
    
    # D'abord la map (fond)
    gamemap.render(screen, (1084, 800))
    
    # Ensuite le joueur (par dessus)
    player_group.draw(screen)

    # Rafraichissement final
    pygame.display.flip()

# Fin du programme
pygame.quit()
sys.exit()