import json

from menu.music_menu import SoundManager

from core.combat_room import CombatRoom
from core.player import Player
import pygame
import os
from game.map import Map
import copy

import math

from core.enemy import EnemyFactory

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Game:

    def __init__(self, screen, level, save_data=None):

        self.sound = SoundManager()
        self.sound.load_sounds()

        self.screen = screen
        self.level_id = level.get("id")

        self.move_speed = 0.04

        self.animations = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }

        self.offset_x = 0
        self.offset_y = 0

        self.paused = False
        self.exit_to_menu = False
        self.pause_resume_rect = None
        self.pause_quit_rect = None
        self.pause_save_rect = None

        self.player = Player()

        self.show_inventory = False
        self.inventory_bg = pygame.image.load("assets/inventaire.png").convert_alpha()

        self.item_to_image = {
            "Potion": "P",
            "Épée": "E",
            "Grande Épée": "E2",
            "Massue": "E3",
            "Potion": "P",
            "Bouclier": "B",
            "Clé": "K",
            "Amulette": "!"
        }

        self.images = {
                    "K": pygame.image.load(os.path.join(BASE_DIR, "assets/cle.png")).convert_alpha(),
                    "P": pygame.image.load(os.path.join(BASE_DIR, "assets/potion.png")).convert_alpha(),
                    "T": pygame.image.load(os.path.join(BASE_DIR, "assets/tresor.png")).convert_alpha(),
                    "E": pygame.image.load(os.path.join(BASE_DIR, "assets/epee.png")).convert_alpha(),
                    "E2": pygame.image.load(os.path.join(BASE_DIR, "assets/epee2.png")).convert_alpha(),
                    "E3": pygame.image.load(os.path.join(BASE_DIR, "assets/epee3.png")).convert_alpha(),
                    "B": pygame.image.load(os.path.join(BASE_DIR, "assets/bouclier.png")).convert_alpha(),

                    "M": pygame.image.load(os.path.join(BASE_DIR, "assets/monstre.png")).convert_alpha(),
                    "M2": pygame.image.load(os.path.join(BASE_DIR, "assets/monstre2.png")).convert_alpha(),
                    "M3": pygame.image.load(os.path.join(BASE_DIR, "assets/monstre3.png")).convert_alpha(),
                    "M4": pygame.image.load(os.path.join(BASE_DIR, "assets/monstre4.png")).convert_alpha(),
                    "M5": pygame.image.load(os.path.join(BASE_DIR, "assets/monstre5.png")).convert_alpha(),
                    "M6": pygame.image.load(os.path.join(BASE_DIR, "assets/monstre6.png")).convert_alpha(),

                    "X": pygame.image.load(os.path.join(BASE_DIR, "assets/boss.png")).convert_alpha(),
                    "X2": pygame.image.load(os.path.join(BASE_DIR, "assets/boss2.png")).convert_alpha(),
                    "X3": pygame.image.load(os.path.join(BASE_DIR, "assets/boss3.png")).convert_alpha(),

                    "A": pygame.image.load(os.path.join(BASE_DIR, "assets/arrive.png")).convert_alpha(),
                    "D": pygame.image.load(os.path.join(BASE_DIR, "assets/depart.png")).convert_alpha(),
                    "J": pygame.image.load(os.path.join(BASE_DIR, "assets/joueur.png")).convert_alpha(),

                    "bubble": pygame.image.load(os.path.join(BASE_DIR, "assets/bubble.png")).convert_alpha(),
                    "bubble2": pygame.image.load(os.path.join(BASE_DIR, "assets/bubble2.png")).convert_alpha(),

                    "proj_player": pygame.image.load(os.path.join(BASE_DIR, "assets/player_proj.png")).convert_alpha(),
                    "proj_enemy": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_enemy.png")).convert_alpha(),
                    "proj_enemy2": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_enemy2.png")).convert_alpha(),
                    "proj_enemy3": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_enemy3.png")).convert_alpha(),
                    "proj_enemy4": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_enemy4.png")).convert_alpha(),
                    "proj_enemy5": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_enemy5.png")).convert_alpha(),
                    "proj_enemy6": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_enemy6.png")).convert_alpha(),

                    "proj_boss": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_boss.png")).convert_alpha(),
                    "proj_boss2": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_boss2.png")).convert_alpha(),
                    "proj_boss3": pygame.image.load(os.path.join(BASE_DIR, "assets/proj_boss3.png")).convert_alpha(),
                    "boss_icon": pygame.image.load(os.path.join(BASE_DIR, "assets/boss_icon.png")).convert_alpha(),
                    "inventaire": pygame.image.load(os.path.join(BASE_DIR, "assets/inventaire.png")).convert_alpha(),

                    "heart": pygame.image.load(os.path.join(BASE_DIR, "assets/heart.png")).convert_alpha(),
                    "heart2": pygame.image.load(os.path.join(BASE_DIR, "assets/heart2.png")).convert_alpha(),
                    "coin": pygame.image.load(os.path.join(BASE_DIR, "assets/coin.png")).convert_alpha(),
                    "bag": pygame.image.load(os.path.join(BASE_DIR, "assets/bag.png")).convert_alpha(),
                    "!": pygame.image.load(os.path.join(BASE_DIR, "assets/amulette.png")).convert_alpha(),

                    "T1": pygame.image.load(os.path.join(BASE_DIR, "assets/teleport.png")).convert_alpha(),
                    "T2": pygame.image.load(os.path.join(BASE_DIR, "assets/teleport2.png")).convert_alpha(),
                    "T3": pygame.image.load(os.path.join(BASE_DIR, "assets/teleport3.png")).convert_alpha(),
                    "T4": pygame.image.load(os.path.join(BASE_DIR, "assets/teleport4.png")).convert_alpha(),
                    
                    "0": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/aaatue_hydra.png")).convert_alpha(),
                    "1": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/altar_makhleb_flame_3.png")).convert_alpha(),
                    "2": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/altar_okawaru.png")).convert_alpha(),
                    "3": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/altar_xom_7.png")).convert_alpha(),
                    "4": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/blood_fountain_2.png")).convert_alpha(),
                    "5": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/chest_2_open.png")).convert_alpha(),
                    "6": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/crumbled_column.png")).convert_alpha(),
                    "7": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/gold_pile_4.png")).convert_alpha(),
                    "8": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/skeleton_humanoid.png")).convert_alpha(),
                    "9": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/statue_dragon.png")).convert_alpha(),
                    "10": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/zltar_beogh.png")).convert_alpha(),
                    "11": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/zltar_fedhas.png")).convert_alpha(),
                    "12": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/zltar_xom_3.png")).convert_alpha(),
                    "13": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/ztatue_sword.png")).convert_alpha(),
                    "14": pygame.image.load(os.path.join(BASE_DIR, "assets/decors/zzatue_orb_guardian.png")).convert_alpha(),
                    
                }
        
        #------------------------------------------------------------
        # SHEET PLAYER

        self.player_sheet = pygame.image.load(
            "assets/joueur_sheet.png"
        ).convert_alpha()

        self.idle_sheet = pygame.image.load(
            "assets/idle_sheet.png"
        ).convert_alpha()

        self.player_frames = []
        self.idle_frames = []

        frame_count = 10

        #------------------------------------------------------------
        # PLAYER SHEET

        self.player_sheet = pygame.image.load(
            "assets/joueur_sheet.png"
        ).convert_alpha()

        self.animations = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }

        frame_width = self.player_sheet.get_width() // 4
        frame_height = self.player_sheet.get_height() // 4

        directions = ["down", "left", "right", "up"]

        for row, direction in enumerate(directions):

            for col in range(4):

                frame = self.player_sheet.subsurface(
                    (
                        col * frame_width,
                        row * frame_height,
                        frame_width,
                        frame_height
                    )
                )

                self.animations[direction].append(frame)

        #------------------------------------------------------------
        # IDLE SHEET

        self.idle_frames = []

        frame_width = self.idle_sheet.get_width() // 4
        frame_height = self.idle_sheet.get_height() // 4

        directions = ["down", "left", "right", "up"]

        self.idle_animations = {d: [] for d in directions}

        for row, direction in enumerate(directions):
            for col in range(4):
                frame = self.idle_sheet.subsurface(
                    (
                        col * frame_width,
                        row * frame_height,
                        frame_width,
                        frame_height
                    )
                )
                self.idle_animations[direction].append(frame)

        #------------------------------------------------------------
        # ANIMATION

        self.direction = "down"

        self.player_frame_index = 0
        self.player_anim_timer = 0
        self.player_anim_speed = 8

        self.current_frame = self.animations["down"][0]

        #-------------------------------------------------------
        
        self.map = Map(level, self.images)

        self.original_carte = copy.deepcopy(level["carte"])
        self.carte = copy.deepcopy(self.original_carte)

        if save_data and save_data.get("level_id") == self.level_id:
            self.load_game(save_data)
        else:
            print("Aucune sauvegarde trouvée pour ce niveau, nouvelle partie.")

            spawn = level.get("spawn", [1, 1])
            self.player.x = spawn[0]
            self.player.y = spawn[1]

        self.view_width = level.get("view_width", 5)
        self.view_height = level.get("view_height", 5)

        tile_w = screen.get_width() // self.view_width
        tile_h = screen.get_height() // self.view_height
        self.tile_size = max(tile_w, tile_h)

        self.font = pygame.font.SysFont("consolas", 20)

        # scale images sans bug
        for key in self.images:
            if key not in ["COMBAT_BG", "bubble", "bubble2"]:
                img = self.images[key]
                img.set_colorkey(img.get_at((0, 0)))
                self.images[key] = pygame.transform.scale(
                    img,
                    (self.tile_size, self.tile_size)
                )

        for key in self.map.level.get("textures", {}):
            if key not in ["bg_combat"]:
                img = self.map.get_image(key)

                if img:
                    img.set_colorkey(img.get_at((0, 0)))
                    self.map.textures[key] = pygame.transform.scale(
                        img,
                        (self.tile_size, self.tile_size)
            )

        self.prev_x = self.player.x
        self.prev_y = self.player.y

        self.state = "MAP"
        self.game_won = False
        self.game_over = False

        self.message = ""
        self.message_timer = 120

        self.camera_x = 0
        self.camera_y = 0

        self.glow_timer = 0

        self.teleports = level.get("teleports", {})
        self.teleport_cooldown = 20 
        self.non_consumable_tiles = {"T1", "T2", "T3", "T4", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"} 

    #--------------------------
    def get_item_key(self, item_name):
        return self.item_to_image.get(item_name)

    # -------------------------

    def reset_map(self):
            import copy
            self.carte = copy.deepcopy(self.original_carte)

            spawn = self.map.level.get("spawn", [1, 1])

            self.player.x = spawn[0]
            self.player.y = spawn[1]

            self.prev_x = self.player.x
            self.prev_y = self.player.y

            self.player.hp = 5
            self.player.score = 0
            self.player.inventaire.clear()

            self.set_message("Nouvelle partie !")

    #-------------------------

    def update_camera(self):

        target_x = self.player.x - self.view_height / 2.5
        target_y = self.player.y - self.view_width / 2.5

        smooth = 0.08

        self.camera_x += (target_x - self.camera_x) * smooth
        self.camera_y += (target_y - self.camera_y) * smooth
    # -------------------------

    def handle_input(self, event):

        # PAUSE PRIORITAIRE
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.sound.play("pause")
            self.paused = not self.paused
            return

        if self.paused:

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.sound.play("pause")

                mouse_pos = event.pos

                if self.pause_resume_rect and self.pause_resume_rect.collidepoint(mouse_pos):
                    self.paused = False

                elif self.pause_quit_rect and self.pause_quit_rect.collidepoint(mouse_pos):
                    self.save_game()
                    self.exit_to_menu = True

                elif self.pause_save_rect and self.pause_save_rect.collidepoint(mouse_pos):
                    self.save_game()

                elif self.pause_reset_rect and self.pause_reset_rect.collidepoint(mouse_pos):
                    self.reset_map()
                    self.set_message("RESET ! TU PEUT MAINTENANT REPRENDRE")

            return

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_F11:
            return "toggle_fullscreen"
        

        if event.key == pygame.K_i:
            self.show_inventory = not self.show_inventory
            return
        
        if self.game_won:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "main"  # ou menu, ou restart
            return

        if event.key == pygame.K_p:
            msg = self.player.use_potion()
            self.set_message(msg)
            return

    #--------------------------

    def set_message(self, text, duration=120):
        self.message = text
        self.message_timer = duration

    #-------------------------
    def check_teleport(self):
        if self.teleport_cooldown > 0:
            return

        key = f"{int(self.player.x)},{int(self.player.y)}"

        if key in self.teleports:
            dest_x, dest_y = self.teleports[key]

            self.player.x = dest_x
            self.player.y = dest_y

            self.prev_x = dest_x
            self.prev_y = dest_y

            self.teleport_cooldown = 100
            self.set_message("Téléportation !")
            self.sound.play("portal")

    #----------------------------
    # COLISION

    def is_wall(self, x, y):
        size = 0.9

        checks = [
            (x, y),
            (x + size, y),
            (x, y + size),
            (x + size, y + size)
        ]

        for cx, cy in checks:
            grid_x = int(cx)
            grid_y = int(cy)

            if (
                grid_x < 0
                or grid_x >= len(self.carte)
                or grid_y < 0
                or grid_y >= len(self.carte[0])
            ):
                return True

            if self.carte[grid_x][grid_y] == "#":
                return True

        return False

    # ---------------------------
    # UPDATE POUR ETRE A SON ACTIF

    def update(self):
        if self.paused:
            return
        
        self.glow_timer += 0.08
        self.update_camera()

        self.check_teleport()

        
        if self.message:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.message = ""

        if self.player.hp <= 0:
            self.game_over = True

        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_UP]:
            dx -= self.move_speed

        if keys[pygame.K_DOWN]:
            dx += self.move_speed

        if keys[pygame.K_LEFT]:
            dy -= self.move_speed

        if keys[pygame.K_RIGHT]:
            dy += self.move_speed

        length = math.hypot(dx, dy)

        if length > 0:
            dx /= length
            dy /= length

        dx *= self.move_speed
        dy *= self.move_speed

        new_x = self.player.x + dx
        new_y = self.player.y + dy

        old_x = self.player.x
        old_y = self.player.y


        # -------------------------
        # COLLISIONS

        # axe X
        if not self.is_wall(new_x, self.player.y):
            self.player.x = new_x

        # axe Y
        if not self.is_wall(self.player.x, new_y):
            self.player.y = new_y


        grid_x = int(self.player.x)
        grid_y = int(self.player.y)

        case = self.carte[grid_x][grid_y]
        
        # -------------------------
        # WIN
        if case == "A":
            self.player.x = new_x
            self.player.y = new_y
            self.set_message("Victoire !")
            self.game_won = True
            self.sound.play("win")
            return
        
        # -------------------------
        # CASES TELEPORT
        if case in ["T1", "T2"]:
            self.player.x = new_x
            self.player.y = new_y
            self.check_teleport()
            return

    # -------------------------
    # COMBAT PRIORITAIRE
        if case in ["M", "X", "X2", "X3", "M2", "M3", "M4", "M5", "M6"]:
            self.prev_x, self.prev_y = old_x, old_y
            self.player.x, self.player.y = grid_x, grid_y
            self.launch_combat(case)
            return

    # -------------------------
    # OBJETS
        msg = self.player.interact(case)

        if msg:
            self.set_message(msg)
            self.sound.play("item_collect")

            if case not in self.non_consumable_tiles:
                self.carte[grid_x][grid_y] = "C"

    # ------------------------------
    # PLAYER IMAGES + DIRECTION
        moving = dx != 0 or dy != 0

        # direction
        if dx < 0:
            self.direction = "up"

        elif dx > 0:
            self.direction = "down"

        elif dy < 0:
            self.direction = "left"

        elif dy > 0:
            self.direction = "right"

        # -------------------------
        # ANIMATION PLAYER

        if moving:
            frames = self.animations[self.direction] 
        else:
            frames = self.idle_animations[self.direction] 

    
        self.player_anim_timer += 1

        if self.player_anim_timer >= self.player_anim_speed:

            self.player_anim_timer = 0

            self.player_frame_index = (
                self.player_frame_index + 1
            ) % len(frames)


        self.current_frame = frames[self.player_frame_index]

    #------------------------------
    # PASSER LE RELAIS A COMBATROOM

    def launch_combat(self, enemy_type):

        enemy = EnemyFactory.create(enemy_type)

        combat = CombatRoom(
            self.screen,
            self.player,
            self.idle_animations,
            self.images,
            enemy,
            self.sound,
            self.map
        )

        result = combat.run()

        if result == "WIN":
            self.set_message(f"{enemy.name} vaincu !")
            self.carte[self.player.x][self.player.y] = "C"

        elif result == "FLEE":
            self.set_message("Fuite !")
            self.player.x, self.player.y = self.prev_x, self.prev_y

        elif result == "LOSE":
            self.game_over = True

    #--------------------------

    def save_game(self):
        data = {
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "hp": self.player.hp,
                "score": self.player.score,
                "inventaire": list(self.player.inventaire) 
            },
            "level_id": self.map.level_id,
            "carte": self.carte
        }

        filename = f"save_level_{self.map.level_id}.json"

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        self.set_message("Partie sauvegardée !")

    
    #--------------------------
    def load_game(self, data=None):

        if data is None:
            filename = f"save_level_{self.level_id}.json"

            if not os.path.exists(filename):
                return

            with open(filename, "r") as f:
                data = json.load(f)

        import copy
        self.carte = copy.deepcopy(data["carte"])


        # --- APPLY DATA ---
        self.player.x = data["player"]["x"]
        self.player.y = data["player"]["y"]
        self.player.hp = data["player"]["hp"]
        self.player.score = data["player"]["score"]
        self.player.inventaire = list(data["player"]["inventaire"])

        self.set_message("Partie chargée !")


    # -------------------------

    def draw(self):
        self.screen.fill((15, 15, 25))

        offset_x = (self.screen.get_width() - self.view_width * self.tile_size) // 2
        offset_y = (self.screen.get_height() - self.view_height * self.tile_size) // 2

        start_x = int(self.camera_x)
        start_y = int(self.camera_y)

        for i in range(start_x, start_x + self.view_height + 2):
            for j in range(start_y, start_y + self.view_width + 2):

                # IMPORTANT
                if not (0 <= i < len(self.carte)):
                    continue

                if not (0 <= j < len(self.carte[i])):
                    continue

                rect = pygame.Rect(
                    int((j - self.camera_y) * self.tile_size + offset_x),
                    int((i - self.camera_x) * self.tile_size + offset_y),
                    self.tile_size,
                    self.tile_size
                )

                case = self.carte[i][j]

                # sol
                sol = self.map.get_image("C")
                if sol:
                    self.screen.blit(sol, rect)

                # objet
                image = self.map.get_image(case)
                if case != "C" and image:
                    self.screen.blit(image, rect)

                # glow
                if case == "K":
                    import math
                    scale = 1.0 + 0.15 * math.sin(self.glow_timer)
                    size = int(self.tile_size * scale)

                    glow_img = pygame.transform.scale(image, (size, size))
                    glow_rect = glow_img.get_rect(center=rect.center)

                    self.screen.blit(glow_img, glow_rect)

        #---------------------------------------------------------------
        # JOUEUR DRAW 

        player_draw_x = int(
            (self.player.y - self.camera_y) * self.tile_size + offset_x
        )

        player_draw_y = int(
            (self.player.x - self.camera_x) * self.tile_size + offset_y
        )

        player_rect = pygame.Rect(
            player_draw_x,
            player_draw_y,
            self.tile_size,
            self.tile_size
        )

        frame = self.current_frame

        scaled = pygame.transform.scale(
            frame,
            (self.tile_size * 1.2, self.tile_size * 1.2)
        )

        self.screen.blit(scaled, scaled.get_rect(center=player_rect.center))


        # -------------------------
        # HUD (TOUJOURS EN DERNIER)
        # BULLE STAT

        x, y = 20, 20
        spacing = 100

        icon_size = 40

        heart = pygame.transform.scale(self.images["heart"], (icon_size, icon_size))
        coin = pygame.transform.scale(self.images["coin"], (icon_size, icon_size))
        bag = pygame.transform.scale(self.images["bag"], (icon_size, icon_size))   # A REUTILISER

        # VIE
        self.screen.blit(heart, (x, y))
        vie_text = self.font.render(str(self.player.hp), True, (255, 255, 255))
        self.screen.blit(vie_text, (x + 45, y + 8))

        # SCORE
        self.screen.blit(coin, (x + spacing, y))
        score_text = self.font.render(str(self.player.score), True, (255, 255, 255))
        self.screen.blit(score_text, (x + spacing + 45, y + 8))

        # INVENTAIRE
        if self.show_inventory:

            # taille max (80% de l'écran)
            max_w = int(self.screen.get_width() * 0.8)
            max_h = int(self.screen.get_height() * 0.8)

            # garder ratio
            img_w, img_h = self.inventory_bg.get_size()
            scale = min(max_w / img_w, max_h / img_h)

            new_size = (int(img_w * scale), int(img_h * scale))
            inv_img = pygame.transform.smoothscale(self.inventory_bg, new_size)

            # centrer
            inv_rect = inv_img.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))

            self.screen.blit(inv_img, inv_rect)

            # -------------------------
            # GRID SETTINGS (avec scale appliqué UNE fois)
            cols = 8
            rows = 5

            slot_size = int(inv_img.get_width() * 0.13)
            padding = int(slot_size * 0.09)

            start_x = inv_rect.left + int(inv_img.get_width() * 0.02)
            start_y = inv_rect.top + int(inv_img.get_height() * 0.14)


            # -------------------------
            # DRAW ITEMS
            for index, item in enumerate(self.player.inventaire):

                col = index % cols
                row = index // cols

                slot_x = start_x + col * (slot_size + padding)
                slot_y = start_y + row * (slot_size + padding)

                img = self.images.get(self.get_item_key(item))

                if img:
                    icon_size = int(slot_size * 0.9)
                    icon = pygame.transform.scale(img, (icon_size, icon_size))

                    icon_rect = icon.get_rect(center=(
                        slot_x + slot_size // 2,
                        slot_y + slot_size // 2
                    ))

                    self.screen.blit(icon, icon_rect)
        # -------------------------
        # MESSAGE BULLE RECUP

        if self.message:

            bubble = self.images.get("bubble2")

            msg_surf = self.font.render(self.message, True, (255, 255, 255))

            x, y = 350, 30

            if bubble:
                # taille dynamique de la bulle
                padding_x = 40
                padding_y = 30

                bubble_scaled = pygame.transform.smoothscale(
                    bubble,
                    (msg_surf.get_width() + padding_x, msg_surf.get_height() + padding_y)
                )

                rect = bubble_scaled.get_rect(topleft=(x, y))
                self.screen.blit(bubble_scaled, rect)

                # texte centré dans la bulle
                text_rect = msg_surf.get_rect(center=rect.center)
                self.screen.blit(msg_surf, text_rect)

            else:
                # fallback
                self.screen.blit(msg_surf, (x, y))

        # -------------------------
        # PAUSE OVERLAY
        if self.paused:
            self.draw_pause_menu()

#-------------------------

    def draw_pause_menu(self):

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("consolas", 40, bold=True)
        small = pygame.font.SysFont("consolas", 25)

        text = font.render("PAUSE", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=(self.screen.get_width()//2, 150)))

        self.pause_resume_rect = pygame.Rect(self.screen.get_width()//2 - 100, 230, 200, 40)
        self.pause_quit_rect = pygame.Rect(self.screen.get_width()//2 - 100, 290, 200, 40)

        pygame.draw.rect(self.screen, (40, 80, 160), self.pause_resume_rect, border_radius=8)
        pygame.draw.rect(self.screen, (40, 80, 160), self.pause_quit_rect, border_radius=8)

        resume_text = small.render("REPRENDRE", True, (255, 255, 255))
        quit_text = small.render("QUITTER MENU", True, (255, 255, 255))

        self.screen.blit(resume_text, resume_text.get_rect(center=self.pause_resume_rect.center))
        self.screen.blit(quit_text, quit_text.get_rect(center=self.pause_quit_rect.center))

        self.pause_save_rect = pygame.Rect(self.screen.get_width()//2 - 100, 350, 200, 40)

        pygame.draw.rect(self.screen, (40, 80, 160), self.pause_save_rect, border_radius=8)

        save_text = small.render("SAUVEGARDER", True, (255, 255, 255))
        self.screen.blit(save_text, save_text.get_rect(center=self.pause_save_rect.center))

        self.pause_reset_rect = pygame.Rect(self.screen.get_width()//2 - 100, 410, 200, 40)

        pygame.draw.rect(self.screen, (160, 60, 60), self.pause_reset_rect, border_radius=8)

        reset_text = small.render("RESET LEVEL", True, (255, 255, 255))
        self.screen.blit(reset_text, reset_text.get_rect(center=self.pause_reset_rect.center))

#-------------------------

    def draw_win_screen(self):

        # overlay sombre + léger jaune
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((20, 20, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # titre
        font_big = pygame.font.SysFont("consolas", 70, bold=True)
        text = font_big.render("VICTOIRE", True, (255, 215, 0))

        rect = text.get_rect(center=(
            self.screen.get_width() // 2,
            self.screen.get_height() // 2 - 40
        ))

        self.screen.blit(text, rect)

        # sous-texte
        font_small = pygame.font.SysFont("consolas", 25)
        sub = font_small.render("Le donjon est terminé ! redirection au menu...", True, (220, 220, 220))

        sub_rect = sub.get_rect(center=(
            self.screen.get_width() // 2,
            self.screen.get_height() // 2 + 20
        ))

        self.screen.blit(sub, sub_rect)
#----------------------------

    def draw_game_over(self):

        # overlay sombre + rouge
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((40, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        # titre
        font_big = pygame.font.SysFont("consolas", 70, bold=True)
        text = font_big.render("GAME OVER", True, (255, 50, 50))

        rect = text.get_rect(center=(
            self.screen.get_width() // 2,
            self.screen.get_height() // 2 - 40
        ))

        self.screen.blit(text, rect)

        # sous-texte
        font_small = pygame.font.SysFont("consolas", 25)
        sub = font_small.render("Vous avez été vaincu...", True, (200, 200, 200))

        sub_rect = sub.get_rect(center=(
            self.screen.get_width() // 2,
            self.screen.get_height() // 2 + 20
        ))

        self.screen.blit(sub, sub_rect)
