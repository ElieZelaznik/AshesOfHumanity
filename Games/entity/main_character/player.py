import pygame
from pytmx.util_pygame import load_pygame

# --- CONFIGURATION ---

# Chemin vers tes images (par rapport à main.py)
DOSSIER_IMG = "Games/entity/main_character/animations/"

ANIMATIONS_DATA = {
    "idle": { "file": "Idle.png", "count": 6, "speed": 0.1, "mode": "loop" },
    "run":  { "file": "Run.png",  "count": 10, "speed": 0.2, "mode": "loop" },
    "jump": { "file": "Jump.png", "count": 10, "speed": 0.1, "mode": "once" },
    "attack": { "file": "Attack_1.png", "count": 3, "speed": 0.1, "mode": "once" },
    "dead": { "file": "Dead.png", "count": 5, "speed": 0.1, "mode": "once" },
    "recharge": { "file": "Recharge.png", "count": 17, "speed": 0.1, "mode": "once" },
    "shoot": { "file": "Shot.png", "count": 4, "speed": 0.1, "mode": "once" },
    "shoot_3_loop": { "file": "Shot.png", "count": 4, "speed": 0.1, "mode": "combo" },
}

# Configuration des touches
KEY_MAPPING = {
    # --- DÉPLACEMENTS (ZQSD) ---
    # Tout le monde est en "run" maintenant pour marcher normalement
    pygame.K_d: {"anim": "run", "dx":  5, "dy":  0, "flip": False},
    pygame.K_q: {"anim": "run", "dx": -5, "dy":  0, "flip": True},
    pygame.K_z: {"anim": "run", "dx":  0, "dy": -5, "flip": None}, # Modifié : jump -> run
    pygame.K_s: {"anim": "run", "dx":  0, "dy":  5, "flip": None}, # Modifié : jump -> run

    # --- ACTIONS (Mode "Once" / Bloquant) ---
    
    # SAUT (ESPACE) : Le saut se fait sur place (dx=0, dy=0)
    # Note : Avec ton système actuel, le joueur ne pourra pas bouger PENDANT le saut
    pygame.K_SPACE: {"anim": "jump",   "dx": 0, "dy": 0, "flip": None},

    # ATTAQUE (Touche E)
    pygame.K_e:     {"anim": "attack", "dx": 0, "dy": 0, "flip": None},

    # AUTRES ACTIONS
    pygame.K_r:     {"anim": "recharge",     "dx": 0, "dy": 0, "flip": None},
    pygame.K_f:     {"anim": "shoot",        "dx": 0, "dy": 0, "flip": None},
    pygame.K_c:     {"anim": "shoot_3_loop", "dx": 0, "dy": 0, "flip": None},
    pygame.K_k:     {"anim": "dead",         "dx": 0, "dy": 0, "flip": None},
}


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Stockage des animations chargées
        self.animations = {} 
        self.load_images()

        # État initial
        self.is_busy = False
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
        
        # 1. SI ON EST OCCUPÉ, ON NE FAIT RIEN (Verrouillage)
        if self.is_busy:
            return
        
        keys = pygame.key.get_pressed()
        action_triggered = False

        # On initialise le mouvement voulu à 0 pour ce tour de boucle
        movement_x = 0
        movement_y = 0

        for key, data in KEY_MAPPING.items():
            if keys[key]:
                
                # --- A. GESTION INTELLIGENTE DE L'ORIENTATION ---
                # Si flip est None, on ne touche à rien (on garde l'ancien flip)
                if data["flip"] is not None:
                    self.flip = data["flip"]
                
                target_anim_mode = ANIMATIONS_DATA[data["anim"]].get("mode", "loop")

                # --- B. CAS ACTIONS BLOQUANTES ---
                if target_anim_mode in ["once", "combo"]:
                    self.current_action = data["anim"]
                    self.is_busy = True 
                    self.frame_index = 0
                    self.animation_speed = ANIMATIONS_DATA[data["anim"]]["speed"]
                    
                    if target_anim_mode == "combo":
                        self.repeat_counter = 3
                    
                    action_triggered = True
                    return 

                # --- C. CAS MOUVEMENTS ---
                else:
                    movement_x += data["dx"]
                    movement_y += data["dy"]

                    if self.current_action != data["anim"]:
                        self.current_action = data["anim"]
                        self.frame_index = 0
                        self.animation_speed = ANIMATIONS_DATA[data["anim"]]["speed"]
                    
                    action_triggered = True
                    
                    # --- D. LE BREAK (DIAGONALES) ---
                    # break # (Optionnel pour les diagonales)
        
        # Retour au repos si aucune touche n'est active
        if not action_triggered:
            if self.current_action != "idle":
                self.current_action = "idle"
                self.frame_index = 0
                self.animation_speed = ANIMATIONS_DATA["idle"]["speed"]
        
        # 2. APPLICATION DU MOUVEMENT ET DES COLLISIONS
        # C'est ici qu'on utilise nos variables accumulées
        self.move(movement_x, movement_y)
    
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
        
        # 1. On attend que le timer soit rempli pour changer d'image
        if self.timer >= 1:
            self.timer = 0
            self.frame_index += 1
            
            # On récupère les infos de l'animation en cours
            current_anim_data = ANIMATIONS_DATA[self.current_action]
            frames_count = len(self.animations[self.current_action])
            mode = current_anim_data.get("mode", "loop")
            
            # 2. FIN DE L'ANIMATION (On a dépassé la dernière image)
            if self.frame_index >= frames_count:
                
                # CAS A : C'est une boucle infinie (Idle, Run)
                if mode == "loop":
                    self.frame_index = 0 # On recommence au début
                
                # CAS B : C'est un combo (répétition X fois)
                elif mode == "combo":
                    if self.repeat_counter > 0:
                        self.repeat_counter -= 1 # On décompte une fois
                        self.frame_index = 0     # On relance l'anim
                    else:
                        # Compteur fini : On libère le joueur
                        self.is_busy = False
                        self.current_action = "idle"
                        self.frame_index = 0
                        self.animation_speed = ANIMATIONS_DATA["idle"]["speed"]

                # CAS C : C'est une action unique (Once) - (Attack, Dead, etc.)
                else:
                    self.is_busy = False # LIBÉRÉ !
                    self.current_action = "idle" # Retour force au repos
                    self.frame_index = 0
                    self.animation_speed = ANIMATIONS_DATA["idle"]["speed"]

        # 3. MISE A JOUR GRAPHIQUE
        # C'est ici que le 'flip' décidé dans get_input s'applique visuellement
        current_img = self.animations[self.current_action][int(self.frame_index)]
        
        if self.flip:
            self.image = pygame.transform.flip(current_img, True, False)
        else:
            self.image = current_img

    def update(self):
        self.get_input()
        self.animate()