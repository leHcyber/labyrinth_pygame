import pygame

TITLE_ASCII = [
" ▄█          ▄████████ ▀█████████▄  ▄██   ▄      ▄████████  ▄█  ███▄▄▄▄       ███        ▄█    █▄       ▄████████ ",
"███         ███    ███   ███    ███ ███   ██▄   ███    ███ ███  ███▀▀▀██▄ ▀█████████▄   ███    ███     ███    ███ ",
"███         ███    ███   ███    ███ ███▄▄▄███   ███    ███ ███▌ ███   ███    ▀███▀▀██   ███    ███     ███    █▀  ",
"███         ███    ███  ▄███▄▄▄██▀  ▀▀▀▀▀▀███  ▄███▄▄▄▄██▀ ███▌ ███   ███     ███   ▀  ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ",
"███       ▀███████████ ▀▀███▀▀▀██▄  ▄██   ███ ▀▀███▀▀▀▀▀   ███▌ ███   ███     ███     ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ",
"███         ███    ███   ███    ██▄ ███   ███ ▀███████████ ███  ███   ███     ███       ███    ███     ███    █▄  ",
"███▌    ▄   ███    ███   ███    ███ ███   ███   ███    ███ ███  ███   ███     ███       ███    ███     ███    ███ ",
"█████▄▄██   ███    █▀  ▄█████████▀   ▀█████▀    ███    ███ █▀    ▀█   █▀     ▄████▀     ███    █▀      ██████████ ",
"▀                                               ███    ███                                                         "
]


QUIT_ASCII = [
"            ▀▀  ██   ",
"▄████ ██ ██ ██ ▀██▀▀ ",
"██ ██ ██ ██ ██  ██   ",
"▀████ ▀██▀█ ██▄ ██   ",
"   ██                ",
"   ▀▀                "
]

PLAY_ASCII = [
"█████▄ ██     ▄████▄ ██  ██ ",
"██▄▄█▀ ██     ██▄▄██  ▀██▀  ",
"██     ██████ ██  ██   ██   "
]

#---------------
# TITLE DRAW

def draw_title(screen):
    font = pygame.font.SysFont("consolas", 10, bold=True)

    y = 40

    for line in TITLE_ASCII:
        shadow = font.render(line, True, (0, 0, 0))
        screen.blit(shadow, shadow.get_rect(center=(screen.get_width() // 2 + 2, y + 2)))

        text = font.render(line, True, (40, 80, 160))
        screen.blit(text, text.get_rect(center=(screen.get_width() // 2, y)))

        y += 11


#----------------
# ASCII BUTTON DRAW

def draw_ascii_button(screen, ascii_art, y, selected, hover):
    font = pygame.font.SysFont("consolas", 14, bold=True)

    base_color = (180, 180, 200)

    if selected:
        color = (70, 170, 255)
    elif hover:
        color = (120, 200, 255)
    else:
        color = base_color

    x = screen.get_width() // 2

    line_height = 16
    total_height = len(ascii_art) * line_height

    start_y = y

    # draw
    for i, line in enumerate(ascii_art):
        text = font.render(line, True, color)
        rect = text.get_rect(center=(x, start_y + i * line_height))
        screen.blit(text, rect)

    # rect FIXE
    return pygame.Rect(
        x - 200,
        y - 10,
        400,
        total_height + 20
    )


#---------------------
# DRAW MENU

def draw_menu(screen, selected):

    draw_title(screen)
    mouse = pygame.mouse.get_pos()

    play_rect = pygame.Rect(0, 0, 0, 0)
    quit_rect = pygame.Rect(0, 0, 0, 0)

    # ------------------------------
    # 1er pass juste pour récupérer les rects
    play_rect = draw_ascii_button(screen, PLAY_ASCII, 310, selected == 0, False)
    quit_rect = draw_ascii_button(screen, QUIT_ASCII, 375, selected == 2, False)

    # hover calculé APRÈS
    play_hover = play_rect.collidepoint(mouse)
    quit_hover = quit_rect.collidepoint(mouse)

    # redraw FINAL
    play_rect = draw_ascii_button(screen, PLAY_ASCII, 310, selected == 0, play_hover)
    quit_rect = draw_ascii_button(screen, QUIT_ASCII, 375, selected == 2, quit_hover)

    #---------------------------
    # BOUTON NIVEAU DRAW

    font = pygame.font.SysFont("consolas", 18, bold=True)

    level_rect = pygame.Rect(screen.get_width() // 2 - 80,screen.get_height() - 55,160,40)

    level_hover = level_rect.collidepoint(mouse)

    level_color = (0, 140, 255) if level_hover else (40, 40, 60)

    pygame.draw.rect(screen, level_color, level_rect, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), level_rect, 2, border_radius=8)

    level_text = font.render("NIVEAUX", True, (255, 255, 255))
    screen.blit(level_text, level_text.get_rect(center=level_rect.center))

    #-------------------
    # INFO / SETTINGS DRAW


    small_font = pygame.font.SysFont("consolas", 18, bold=True)

    info_rect = pygame.Rect(20, screen.get_height() - 50, 120, 35)
    settings_rect = pygame.Rect(screen.get_width() - 140, screen.get_height() - 50, 120, 35)

    info_hover = info_rect.collidepoint(mouse)
    settings_hover = settings_rect.collidepoint(mouse)

    info_color = (0, 120, 200) if info_hover else (40, 40, 60)
    settings_color = (0, 120, 200) if settings_hover else (40, 40, 60)

    pygame.draw.rect(screen, info_color, info_rect, border_radius=8)
    pygame.draw.rect(screen, settings_color, settings_rect, border_radius=8)

    pygame.draw.rect(screen, (0, 0, 0), info_rect, 2, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), settings_rect, 2, border_radius=8)

    info_text = small_font.render("INFO", True, (255, 255, 255))
    settings_text = small_font.render("SETTINGS", True, (255, 255, 255))

    screen.blit(info_text, info_text.get_rect(center=info_rect.center))
    screen.blit(settings_text, settings_text.get_rect(center=settings_rect.center))

    return play_rect, level_rect, quit_rect, info_rect, settings_rect
