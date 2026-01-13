import pygame
#Les objets (mouvement)

class joueur(pygame.sprite.Sprite):#Sprite = element graphique du jeu (ici, le joueur)
    def __init__(self):
        super().__init__()

        #THEORIE
        
        def move_right(self):
            self.position[0] += 3
        def move_left(self):
            self.position[0] -= 3
        def move_up(self):
            self.position[1] -= 3
        def move_down(self):
            self.position[1] += 3
            #Faut penser à rajouter au main 
            #la variable "self.position = [x,y]
        
        def touches_utilises(self):
            pressed = pygame.key.get_pressed()#récupère toutes les touches enclenché par le joueur

            if pressed[pygame.K_UP]:
                self.player.move_up()
            elif pressed[pygame.K_DOWN]:
                self.player.move_down()
            elif pressed[pygame.K_LEFT]:
                self.player.move_left()
            elif pressed[pygame.K_RIGHT]:
                self.player.move_right()
        #PRATIQUE
        
        