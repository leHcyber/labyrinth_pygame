from fileinput import filename

import pygame
import os
import importlib
import json

SAVE_FILE = "save.json"

data = None

if os.path.exists(SAVE_FILE):   
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    except:
        data = None

from menu.draw_menu import draw_menu
from menu.text_menu import RULES_TEXT, SETTINGS_TEXT
from game.engine import Game

from game.map import Map
from menu.music_menu import MusicManager, SoundManager

from menu.scene_menu import (
    draw_background,
    draw_text_screen,
    draw_online_levels,
    draw_offline_levels
)

level_buttons = []
levels_state = "offline"
menu_state = "main"
offline_selected = 0
selected_level = 0
current_state_music = None
selected = -1
running = True
scroll_offset = 0

# -------------------------
# SET UP LA FENETRE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH, HEIGHT = 914, 539
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labyrinthe")
clock = pygame.time.Clock()

# -------------------------
# DEF DU PLEIN ECRAN
fullscreen = False

def toggle_fullscreen():
    global screen, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

#----------------------------------------------
# FRAME

menu_frames = []
bg_folder = os.path.join(BASE_DIR, "assets/menu_bg")

if os.path.exists(bg_folder):
    for f in sorted(os.listdir(bg_folder)):
        if f.endswith(".png"):
            img = pygame.image.load(os.path.join(bg_folder, f)).convert()
            scale = max(WIDTH / img.get_width(), HEIGHT / img.get_height())
            img = pygame.transform.scale(img, (
                int(img.get_width() * scale),
                int(img.get_height() * scale)
            ))
            menu_frames.append(img)

frame = 0
timer = 0

# -------------------------
# SET MUSIC

music = MusicManager(BASE_DIR)
music.play("assets/music/menu.mp3")

# -------------------------
# LOAD LEVELS
def load_levels():
    levels = []
    folder = os.path.join(BASE_DIR, "levels")

    if not os.path.exists(folder):
        print("Dossier levels introuvable")
        return levels

    for file in sorted(os.listdir(folder)):
        if file.startswith("level") and file.endswith(".py"):
            try:
                module = importlib.import_module(f"levels.{file[:-3]}")
                importlib.reload(module)

                if hasattr(module, "level_data"):
                    levels.append(module.level_data)
                else:
                    print(f"{file} n'a pas de level_data")

            except Exception as e:
                print(f"Erreur dans {file} :", e)

    return levels

LEVELS = load_levels()

if not LEVELS:
    raise Exception("Aucun level chargé")

save_data = data

level = None

if data and data.get("level_id"):
    level = next((l for l in LEVELS if l.get("id") == data["level_id"]), None)

if level is None:
    print("Level introuvable, fallback level")
    level = LEVELS[0]

# -------------------------
# GAME LOOP
def run_level(level, save_data=None):

    filename = f"save_level_{level.get('id')}.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            save_data = json.load(f)
    else:
        save_data = None

    game = Game(screen, level, save_data)

    music.play("assets/music/game.mp3")

    while True:
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                return "quit"

            action = game.handle_input(e)
            if action == "toggle_fullscreen":
                toggle_fullscreen()

        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

        if game.game_won:
            game.draw()
            game.draw_win_screen()

            sound = SoundManager()
            sound.load_sounds()

            sound.play("win")
            pygame.display.flip()
            pygame.time.wait(3000)

            game.reset_map()

            music.play("assets/music/menu.mp3")
            return "menu"
        
        if game.game_over:
            game.draw()
            game.draw_game_over()

            sound = SoundManager()
            sound.load_sounds()

            sound.play("game_over")
            
            pygame.display.flip()
            pygame.time.wait(3000)

            game.reset_map()

            music.play("assets/music/menu.mp3")
            return "menu"

        if game.exit_to_menu:
            music.play("assets/music/menu.mp3")
            return "menu"
    
# -------------------------
# MAIN LOOP
while running:

    mouse = pygame.mouse.get_pos()
    

    if menu_state == "main":
        frame, timer = draw_background(screen, menu_frames, frame, timer, clock)
        play_r, level_r, quit_r, info_r, set_r = draw_menu(screen, selected)

    elif menu_state == "rules":
        draw_text_screen(screen, "REGLES", RULES_TEXT, scroll_offset, WIDTH, HEIGHT)

    elif menu_state == "settings":
        draw_text_screen(screen, "PARAMETRES", SETTINGS_TEXT, scroll_offset, WIDTH, HEIGHT)

    elif menu_state == "levels":
        draw_online_levels(screen, WIDTH, HEIGHT)

    elif menu_state == "offline_levels":
        level_buttons = draw_offline_levels(screen, LEVELS, mouse, WIDTH, HEIGHT)

    #---------------------
    # EVENTS

    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            running = False

        #--------------------------
        # GLOBAL KEYS

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_F11:
                toggle_fullscreen()

            if e.key == pygame.K_ESCAPE:

                if menu_state in ["rules", "settings", "levels"]:
                    menu_state = "main"
                    scroll_offset = 0

                elif menu_state == "offline_levels":
                    menu_state = "main"

        # -----------------------
        # MAIN MENU TOUCHE

        if menu_state == "main":

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3

                elif e.key == pygame.K_UP:
                    selected = (selected - 1) % 3

                elif e.key == pygame.K_RETURN:

                    if selected == 0:
                        menu_state = "offline_levels"

                    elif selected == 1:
                        menu_state = "rules"

                    elif selected == 2:
                        running = False


            elif e.type == pygame.MOUSEBUTTONDOWN:

                if play_r.collidepoint(e.pos):
                    selected = 0
                    menu_state = "offline_levels"

                elif level_r.collidepoint(e.pos):
                    selected = 1
                    menu_state = "levels"

                elif info_r.collidepoint(e.pos):
                    selected = 1
                    menu_state = "rules"

                elif set_r.collidepoint(e.pos):
                    selected = 1
                    menu_state = "settings"

                elif quit_r.collidepoint(e.pos):
                    selected = 2
                    running = False
                    

        #-------------------------
        # MENU OFFLINE TOUCHE

        elif menu_state == "offline_levels":

            if e.type == pygame.MOUSEBUTTONDOWN:

                for i, rect in enumerate(level_buttons):
                    if rect.collidepoint(mouse):
                        
                        result = run_level(LEVELS[i], save_data)

                        if result == "menu":
                            menu_state = "main"
                        elif result == "quit":
                            running = False

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(LEVELS)

                elif e.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(LEVELS)

                elif e.key == pygame.K_RETURN:
                    result = run_level(LEVELS[selected_level], save_data)

                    if result == "menu":
                        menu_state = "main"
                    elif result == "quit":
                        running = False

        #------------------------
        # SCROLL RULES / SETTINGS

        if e.type == pygame.MOUSEWHEEL:

            if menu_state in ["rules", "settings"]:
                scroll_offset += e.y * 20
                scroll_offset = max(min(scroll_offset, 0), -len(RULES_TEXT)*35 + HEIGHT - 400)
    
    clock.tick(60)
    pygame.display.flip()