import pygame
pygame.init()

pygame.display.set_mode((800,600))#taille de la fenêtre
pygame.display.set_caption("Ashes Of Humanity")#Nom du jeu

running = True
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#Pour que la fenêtre ne se ferme pas
pygame.quit()