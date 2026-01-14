import pygame
from pytmx.util_pygame import load_pygame

# --- CONFIGURATION ---

# Chemin vers tes images (par rapport à main.py)
DOSSIER_IMG = "Games/entity/main_character/animations/"

ANIMATIONS_DATA = {
    "idle": { "file": "Idle.png", "count": 6, "speed": 0.1 },
    "run":  { "file": "Run.png",  "count": 10, "speed": 0.2 },
    "jump": { "file": "Jump.png", "count": 10, "speed": 0.1 },
}

# Configuration des touches
KEY_MAPPING = {
    pygame.K_d: {"anim": "run",  "dx":  5, "dy":  0, "flip": False},
    pygame.K_q: {"anim": "run",  "dx": -5, "dy":  0, "flip": True},
    pygame.K_z: {"anim": "jump", "dx":  0, "dy": -5, "flip": False},
    pygame.K_s: {"anim": "jump", "dx":  0, "dy":  5, "flip": False},
}


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Stockage des animations chargées
        self.animations = {} 
        self.load_images()

        # État initial
        self.current_action = "idle"
        self.frame_index = 0
        self.image = self.animations[self.current_action][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.flip = False
        

        #definir la hitbox sur les pied du joueur
        hitbox_width = self.rect.width // 4               #largeur
        hitbox_height = 20                                #hauteur
        hitbox_x = self.rect.centerx - hitbox_width // 2  # centrer sur les pieds
        hitbox_y = self.rect.bottom - hitbox_height       # placer au bas du joueur



        self.hitbox = pygame.Rect(hitbox_x, hitbox_y,hitbox_width,hitbox_height)

        # Timer d'animation
        self.animation_speed = ANIMATIONS_DATA["idle"]["speed"]
        self.timer = 0
        
        #creation d'une liste qui stocke les rectangle de collision
        self.walls = []
        self.tmx_data = load_pygame('Games/ressource/map/map.tmx')

        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.walls.append(rect)

        


    def load_images(self):
        """Charge les Sprite Sheets et les découpe proprement"""
        for anim_name, data in ANIMATIONS_DATA.items():
            temp_list = []
            full_path = DOSSIER_IMG + data["file"]
            
            try:
                # 1. Chargement de la feuille complète
                sheet = pygame.image.load(full_path).convert_alpha()
                
                # 2. Calculs de découpe
                sheet_width = sheet.get_width()
                sheet_height = sheet.get_height()
                frame_count = data["count"]
                
                # IMPORTANT : Division entière (//) pour éviter le pixel drift
                frame_width = sheet_width // frame_count
                
                # 3. Découpage
                for i in range(frame_count):
                    # On prend un rectangle : (position x, 0, largeur, hauteur)
                    rect = (i * frame_width, 0, frame_width, sheet_height)
                    frame = sheet.subsurface(rect)
                    temp_list.append(frame)
            
            except Exception as e:
                print(f"ERREUR chargement {anim_name} ({full_path}): {e}")
                # Carré rouge de secours en cas de pépin
                surf = pygame.Surface((50, 50))
                surf.fill((255, 0, 0))
                temp_list.append(surf)
            
            self.animations[anim_name] = temp_list

    def get_input(self):
        """Gestion des entrées clavier via le dictionnaire de config"""
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        action_triggered = False

        for key, data in KEY_MAPPING.items():
            if keys[key]:
                # Mouvement
                dx += data["dx"]
                dy += data["dy"]

                # Orientation (Flip)
                self.flip = data["flip"]

                # Changement d'animation si nécessaire
                if self.current_action != data["anim"]:
                    self.current_action = data["anim"]
                    self.frame_index = 0
                    self.animation_speed = ANIMATIONS_DATA[data["anim"]]["speed"]
                
                action_triggered = True
                # On arrête de vérifier les autres touches (priorité à la première trouvée)
                # Enlève le break si tu veux gérer les diagonales parfaitement
                # break 
        
        # Retour au repos si aucune touche n'est active
        if not action_triggered:
            if self.current_action != "idle":
                self.current_action = "idle"
                self.frame_index = 0
                self.animation_speed = ANIMATIONS_DATA["idle"]["speed"]
        
        self.move(dx, dy)
    
    def move(self, dx, dy):
        # --- X ---
        self.hitbox.x += dx
        for wall in self.walls:
            if self.hitbox.colliderect(wall):
                if dx > 0:
                    self.hitbox.right = wall.left
                elif dx < 0:
                    self.hitbox.left = wall.right

        # --- Y ---
        self.hitbox.y += dy
        for wall in self.walls:
            if self.hitbox.colliderect(wall):
                if dy > 0:
                    self.hitbox.bottom = wall.top
                elif dy < 0:
                    self.hitbox.top = wall.bottom
        
        self.rect.midbottom = self.hitbox.midbottom


    def animate(self):
        """Fait défiler les images"""
        self.timer += self.animation_speed
        
        if self.timer >= 1:
            self.timer = 0
            self.frame_index += 1
            
            # Boucle l'animation
            frames_count = len(self.animations[self.current_action])
            if self.frame_index >= frames_count:
                self.frame_index = 0

        # Mise à jour de l'image
        current_img = self.animations[self.current_action][int(self.frame_index)]
        
        if self.flip:
            self.image = pygame.transform.flip(current_img, True, False)
        else:
            self.image = current_img

    def update(self):
        self.get_input()
        self.animate()