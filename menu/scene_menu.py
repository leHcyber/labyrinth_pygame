import pygame

# -------------------------
# BACKGROUND ANIMÉ

def draw_background(screen, menu_frames, frame, timer, clock):

    if not menu_frames:
        screen.fill((10, 10, 20))
        return frame, timer

    screen.blit(menu_frames[frame], (0, 0))

    timer += clock.get_time()
    if timer > 45:
        timer = 0
        frame = (frame + 1) % len(menu_frames)

    return frame, timer


# -------------------------
# TEXT SCREEN (RULES / SETTINGS)

def draw_text_screen(screen, title, lines, scroll_offset, WIDTH, HEIGHT):

    screen.fill((10, 10, 20))

    title_font = pygame.font.SysFont("consolas", 40, bold=True)
    font = pygame.font.SysFont("consolas", 22)

    screen.blit(title_font.render(title, True, (0, 200, 255)),
                (WIDTH//2 - 120, 60))

    y = 160 + scroll_offset

    for line in lines:
        if 100 < y < HEIGHT - 50:
            surf = font.render(line, True, (220, 220, 220))
            screen.blit(surf, surf.get_rect(center=(WIDTH//2, y)))
        y += 35

    # hint (comme dans ton code)
    hint = pygame.font.SysFont("consolas", 18).render(
        "ESC pour retour en arrière", True, (120, 120, 120)
    )
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 510))


# -------------------------
# ONLINE LEVELS (SOON)

def draw_online_levels(screen, WIDTH, HEIGHT):

    screen.fill((10, 10, 20))

    font = pygame.font.SysFont("consolas", 30, bold=True)

    title = font.render("ONLINE LEVELS (SOON)", True, (0, 200, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    msg = pygame.font.SysFont("consolas", 20).render(
        "crée, édit et joue a des labyrinthe en ligne !", True, (180, 180, 180)
    )
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 200))

    hint = pygame.font.SysFont("consolas", 18).render(
        "ESC pour retour en arrière", True, (120, 120, 120)
    )
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 80))


# -------------------------
# OFFLINE LEVELS

def draw_offline_levels(screen, LEVELS, mouse, WIDTH, HEIGHT):

    screen.fill((10, 10, 20))

    font = pygame.font.SysFont("consolas", 30, bold=True)

    title = font.render("SELECT LEVEL", True, (0, 200, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    hint = pygame.font.SysFont("consolas", 18).render(
        "ESC pour retour en arrière", True, (120, 120, 120)
    )
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 80))

    level_buttons = []

    for i in range(len(LEVELS)):

        rect = pygame.Rect(WIDTH // 2 - 100, 150 + i * 70, 200, 50)

        color = (0, 150, 255) if rect.collidepoint(mouse) else (40, 40, 60)

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)

        txt = pygame.font.SysFont("consolas", 22).render(
            f"LEVEL {i + 1}", True, (255, 255, 255)
        )

        screen.blit(txt, txt.get_rect(center=rect.center))

        level_buttons.append(rect)

    return level_buttons