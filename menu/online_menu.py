import pygame


# -------------------------
# ONLINE LEVELS (SOON)

def draw_online_levels(screen, WIDTH, HEIGHT, mouse):

    screen.fill((10, 10, 20))

    font = pygame.font.SysFont("consolas", 30, bold=True)

    title = font.render("ONLINE MENU", True, (0, 200, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    hint = pygame.font.SysFont("consolas", 18).render(
        "ESC pour retour en arrière", True, (120, 120, 120)
    )
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 80))

    buttons = {}

    # -------------------------
    # LEVELS
    rect_levels = pygame.Rect(WIDTH // 2 - 100, 180, 200, 50)
    color = (0, 150, 255) if rect_levels.collidepoint(mouse) else (40, 40, 60)

    pygame.draw.rect(screen, color, rect_levels, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), rect_levels, 2, border_radius=8)

    txt = pygame.font.SysFont("consolas", 22).render("LEVELS", True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect_levels.center))

    buttons["levels"] = rect_levels

    # -------------------------
    # CHAT
    rect_chat = pygame.Rect(WIDTH // 2 - 100, 260, 200, 50)
    color = (0, 150, 255) if rect_chat.collidepoint(mouse) else (40, 40, 60)

    pygame.draw.rect(screen, color, rect_chat, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), rect_chat, 2, border_radius=8)

    txt = pygame.font.SysFont("consolas", 22).render("CHAT", True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect_chat.center))

    buttons["chat"] = rect_chat

    # -------------------------
    # CREATE LEVELS
    rect_create = pygame.Rect(WIDTH // 2 - 100, 340, 200, 50)
    color = (0, 150, 255) if rect_create.collidepoint(mouse) else (40, 40, 60)

    pygame.draw.rect(screen, color, rect_create, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), rect_create, 2, border_radius=8)

    txt = pygame.font.SysFont("consolas", 20).render("CREATE", True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect_create.center))

    buttons["create"] = rect_create

    return buttons
