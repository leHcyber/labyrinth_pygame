import pygame
from core.player import Player, Entity
from core.enemy import *
from menu.music_menu import SoundManager

class CombatRoom:
    def __init__(self, screen, player, idle_animations, images, enemy, sound, game_map):

        self.screen = screen
        self.player = player

        self.idle_animations = idle_animations
        self.idle_index = 0
        self.idle_timer = 0

        self.player_flash_timer = 0
        self.enemy_flash_timer = 0

        self.images = images
        self.sound = sound
        self.map = game_map

        self.projectiles = []

        self.action_locked = False

        self.player_dmg = None
        self.enemy_dmg = None
        self.dmg_timer = 0

        self.enemy = enemy

        self.state = "RUNNING"

        self.font = pygame.font.SysFont("consolas", 20)

        self.turn = "PLAYER"
        self.cooldown = 0

    # -------------------------
    # INPUT

    def handle_event(self, event):

        if self.action_locked:
            return 

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_a:
            self.player_attack()

        elif event.key == pygame.K_b:
            self.block()

        elif event.key == pygame.K_p:
            self.use_potion()

        elif event.key == pygame.K_f:
            self.state = "FLEE"
            self.player.set_message("Fuite !")
    # -------------------------
    # ACTIONS

    def player_attack(self):
        if self.turn != "PLAYER":
            return
        
        self.sound.play("envole")

        player_pos = (180, self.screen.get_height() // 2 + 40)
        enemy_pos = (580, self.screen.get_height() // 2 + 40)

        self.projectiles.append(
            Projectile(
                player_pos[0],
                player_pos[1],
                enemy_pos[0],
                enemy_pos[1],
                owner="PLAYER",
                images=self.images,
                enemy_type=self.enemy.type
            )
        )

        self.action_locked = True

#-------------------------------------------------

    def enemy_attack(self):
        if self.turn != "ENEMY":
            return
        
        self.sound.play("envole")

        enemy_pos = (580, self.screen.get_height() // 2 + 40)
        player_pos = (180, self.screen.get_height() // 2 + 40)

        self.projectiles.append(
            Projectile(
                enemy_pos[0],
                enemy_pos[1],
                player_pos[0],
                player_pos[1],
                owner="ENEMY",
                images=self.images,
                enemy_type=self.enemy.type
            )
        )

        self.action_locked = True

#-------------------------------------------------

    def block(self):

        if self.player.hp <= 0:
            self.state = "LOSE"

    def use_potion(self):

        if self.turn != "PLAYER":
           return

        if "Potion" in self.player.inventaire:
            self.player.hp += 2
            self.player.inventaire.remove("Potion")
            self.player.set_message("+2 vie")
        else:
            self.player.set_message("Pas de potion")

    # -------------------------
    # UPDATE

    def update(self):

        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if self.turn == "ENEMY" and not self.action_locked:
            self.enemy_attack()

        for p in self.projectiles[:]:
            p.update()

            if not p.alive:

                # -------------------------
                # PROJECTILE JOUEUR + DAMAGE

                if p.owner == "PLAYER":

                    self.sound.play("impact")

                    dmg = self.player.get_damage()
                    self.enemy.take_damage(dmg)

                    self.enemy_flash_timer = 10

                    self.enemy_dmg = f"-{dmg}" if dmg > 0 else None
                    self.dmg_timer = 30

                    if self.enemy.is_dead():
                        self.state = "WIN"
                        self.sound.play("disapear")
                        return

                    self.turn = "ENEMY"
                    self.action_locked = False
                    self.cooldown = 20

                # -------------------------
                # PROJECTILE ENNEMI + DAMAGE

                elif p.owner == "ENEMY":

                    self.sound.play("impact")

                    dmg = self.enemy.get_damage()
                    self.player.take_damage(dmg)

                    self.player_flash_timer = 10

                    self.player_dmg = f"-{dmg}" if dmg > 0 else None
                    self.dmg_timer = 30

                    if self.player.is_dead():
                        self.state = "LOSE"
                        return

                    self.turn = "PLAYER"
                    self.action_locked = False
                    self.cooldown = 20

                self.projectiles.remove(p)

    # -------------------------
    # DRAW

    def draw(self):

        # -------------------------
        # FOND COMBAT
 
        bg = self.map.get_image("bg_combat")

        if bg:
            bg_scaled = pygame.transform.smoothscale(
                bg,
                self.screen.get_size()
            )
            self.screen.blit(bg_scaled, (0, 0))
        else:
            self.screen.fill((15, 15, 25))

        #--------------------------
        # PROJECTILE

        for p in self.projectiles:
            p.draw(self.screen)

        # -------------------------
        # BULLE HUD

        bubble = self.images.get("bubble")
        heart_enemy = self.images.get("heart")
        heart_player = self.images.get("heart2")
        boss_icon = self.images.get("boss_icon")

        x, y = 18, 8

        HEART_SIZE = 17
        PAD_X = 50
        PAD_Y = 39

        if not heart_enemy:
            heart_enemy = None
        if not heart_player:
            heart_player = None

        heart_enemy = pygame.transform.scale(heart_enemy, (HEART_SIZE, HEART_SIZE))
        heart_player = pygame.transform.scale(heart_player, (HEART_SIZE, HEART_SIZE))

        # titres
        player_title = self.font.render("PLAYER", True, (100, 200, 255))
        enemy_title = self.font.render(self.enemy.name, True, (255, 100, 100))

        # fond bulle
        width = 305
        height = 160

        if bubble:
            bubble_scaled = pygame.transform.smoothscale(
                bubble,
                (width, height)
            )
            self.screen.blit(bubble_scaled, (x, y))

        base_x = x + PAD_X
        base_y = y + PAD_Y

        # -------------------------
        # TITRES
        self.screen.blit(player_title, (base_x, base_y))
        self.screen.blit(enemy_title, (base_x + 110, base_y))

        # -------------------------
        # COEURS JOUEUR
        for i in range(int(self.player.hp)):

            row = i // 5
            col = i % 5

            self.screen.blit(
                heart_player,
                (
                    base_x + col * (HEART_SIZE + 3),
                    base_y + 25 + row * (HEART_SIZE + 3)
                )
            )

        # -------------------------
        # COEURS ENNEMI
        for i in range(int(self.enemy.hp)):

            row = i // 5
            col = i % 5

            self.screen.blit(
                heart_enemy,
                (
                    base_x + 110 + col * (HEART_SIZE + 3),
                    base_y + 25 + row * (HEART_SIZE + 3)
                )
            )
            
        # -------------------------
        # TITRE ENNEMI

        self.screen.blit(enemy_title, (base_x + 110, base_y))

        # -------------------------
        # ICON BOSS
        if "Boss" in self.enemy.name and boss_icon:
            icon_size = 28
            icon = pygame.transform.scale(boss_icon, (icon_size, icon_size))

            self.screen.blit(icon, (base_x + 110 + enemy_title.get_width() + 5, base_y))

        # -------------------------
        # JOUEUR

        if self.idle_animations and "down" in self.idle_animations:

            frames = self.idle_animations["down"] 

            self.idle_timer += 1

            if self.idle_timer >= 8:
                self.idle_timer = 0
                self.idle_index = (self.idle_index + 1) % len(frames)

            player_img = frames[self.idle_index]

            scale = 5.0

            new_size = (
                int(player_img.get_width() * scale),
                int(player_img.get_height() * scale)
            )

            player_big = pygame.transform.scale(player_img, new_size)

            player_rect = player_big.get_rect(
                center=(180, self.screen.get_height() // 2 + 40)
            )

            self.screen.blit(player_big, player_rect)

            if self.player_flash_timer > 0:
                flash = player_big.copy()
                red = pygame.Surface(flash.get_size(), pygame.SRCALPHA)
                red.fill((255, 0, 0, 120))
                flash.blit(red, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(flash, player_rect)
                self.player_flash_timer -= 1

        else:
            pygame.draw.circle(self.screen,(0, 200, 255),(180, self.screen.get_height() // 2),30)

        # -------------------------
        # ENNEMI

        enemy_type=self.enemy.type
        enemy_img = self.images.get(enemy_type)
        enemy_rect = None

        if enemy_img:
            scale = 1.4
            new_size = (
                int(enemy_img.get_width() * scale),
                int(enemy_img.get_height() * scale)
            )

            enemy_big = pygame.transform.scale(enemy_img, new_size)
            enemy_rect = enemy_big.get_rect(center=(580, self.screen.get_height() // 2 + 40))

            self.screen.blit(enemy_big, enemy_rect)

            if self.enemy_flash_timer > 0:
                flash = enemy_big.copy()
                red = pygame.Surface(flash.get_size(), pygame.SRCALPHA)
                red.fill((255, 0, 0, 120))
                flash.blit(red, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(flash, enemy_rect)
                self.enemy_flash_timer -= 1

        else:
            pygame.draw.circle(self.screen, (255, 80, 80), (580, self.screen.get_height() // 2), 30)

        # -------------------------
        # DEGATS
    
        if self.dmg_timer > 0:

            self.dmg_timer -= 1

            if self.dmg_timer == 0:
                self.player_dmg = None
                self.enemy_dmg = None

            if self.enemy_dmg and enemy_rect:
                dmg_surf = self.font.render(self.enemy_dmg, True, (255, 50, 50))
                dmg_rect = dmg_surf.get_rect(midbottom=(
                    enemy_rect.centerx,
                    enemy_rect.top - 10
                ))
                self.screen.blit(dmg_surf, dmg_rect)

            # dégâts joueur (affiché au dessus du joueur)
            if self.player_dmg and player_rect:
                dmg_surf = self.font.render(self.player_dmg, True, (255, 50, 50))
                dmg_rect = dmg_surf.get_rect(midbottom=(
                    player_rect.centerx,
                    player_rect.top - 10
                ))
                self.screen.blit(dmg_surf, dmg_rect)

        # -------------------------
        # COMMANDES
 
        ui = self.font.render(
            "A= Attaquer  P= Potion  F= Fuir",
            True,
            (200, 200, 200)
        )

        ui_rect = ui.get_rect(center=(
            self.screen.get_width() // 2,
            self.screen.get_height() - 45
        ))

        self.screen.blit(ui, ui_rect)

        # -------------------------
        # MESSAGE PLAYER 

        if self.player.message:

            bubble = self.images.get("bubble2")

            msg_surf = self.font.render(self.player.message, True, (255, 255, 255))

            x, y = 400, 30

            if bubble:
                bubble_scaled = pygame.transform.smoothscale(
                    bubble,
                    (msg_surf.get_width() + 40, msg_surf.get_height() + 30)
                )

                rect = bubble_scaled.get_rect(topleft=(x, y))
                self.screen.blit(bubble_scaled, rect)

                text_rect = msg_surf.get_rect(center=rect.center)
                self.screen.blit(msg_surf, text_rect)
            else:
                self.screen.blit(msg_surf, (x, y))

            self.player.message_timer -= 1
            if self.player.message_timer <= 0:
                self.player.message = ""

    # -------------------------
    # RUN LOOP
 
    def run(self):

        clock = pygame.time.Clock()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                self.handle_event(event)

            self.update()
            self.draw()

            pygame.display.flip()
            clock.tick(60)

            if self.state in ["WIN", "LOSE", "FLEE"]:
                return self.state
            
#--------------------------------------------------------------------------------------------------------------------           

class Projectile:
    def __init__(self, x, y, target_x, target_y, owner, images, speed=8, enemy_type=None):
        self.x = x
        self.y = y

        self.target_x = target_x
        self.target_y = target_y

        self.owner = owner
        self.enemy_type = enemy_type
        self.images = images

        self.speed = speed
        self.radius = 4
        self.alive = True

        dx = target_x - x
        dy = target_y - y
        dist = max((dx**2 + dy**2) ** 0.5, 1)

        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if abs(self.x - self.target_x) < 10 and abs(self.y - self.target_y) < 10:
            self.alive = False

    def draw(self, screen):

        if self.owner == "PLAYER":
            img = self.images.get("proj_player")

        else:
            proj_map = {
                "M": "proj_enemy",
                "M2": "proj_enemy2",
                "M3": "proj_enemy3",
                "M4": "proj_enemy4",
                "M5": "proj_enemy5",
                "M6": "proj_enemy6",
                "X": "proj_boss",
                "X2": "proj_boss2",
                "X3": "proj_boss3"
            }

            img = self.images.get(proj_map.get(self.enemy_type, "proj_enemy"))

        if img:
            scale = 0.7
            w = int(img.get_width() * scale)
            h = int(img.get_height() * scale)
            img_small = pygame.transform.scale(img, (w, h))

            rect = img_small.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(img_small, rect)
        else:
            pygame.draw.circle(screen, (255, 255, 0),
                               (int(self.x), int(self.y)), self.radius)


class Animation:
    def __init__(self, frames, speed=5):
        self.frames = frames
        self.speed = speed
        self.index = 0
        self.timer = 0
        self.finished = False

    def update(self):
        self.timer += 1
        if self.timer >= self.speed:
            self.timer = 0
            self.index += 1

            if self.index >= len(self.frames):
                self.index = len(self.frames) - 1
                self.finished = True

    def get_frame(self):
        return self.frames[self.index]