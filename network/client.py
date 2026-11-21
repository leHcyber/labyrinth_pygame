import socket
import threading
import pygame
import pygame_gui

import json
import time
import os

from network.account import NAME_CHANGE_DELAY

pygame.init()

# ---------------- SOCKET
HOST = "hopper.proxy.rlwy.net"
PORT = 13581

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ACCOUNT_FILE = "network/account.json"

# ---------------- STATE
chat_needs_update = False
connected = False
in_chat = False
username = ""

chat_history = []
users = []

# ---------------- UI GLOBALS
manager = None
screen = None
clock = pygame.time.Clock()

login_input = None
connect_btn = None
modify_btn = None
login_quit_btn = None

chat_box = None
users_box = None
message_input = None
send_btn = None
disconnect_btn = None

info_message = ""


# ---------------- UI UPDATE
def update_chat():
    if chat_box:
        chat_box.set_text("<br>".join(chat_history[-100:]))

def update_users():
    if users_box:
        users_box.set_text("USERS:<br>" + "<br>".join(users))


# ---------------- RECEIVE THREAD
buffer = ""

def receive():
    global buffer, users, connected, chat_needs_update

    while connected:
        try:
            data = client.recv(1024).decode("utf-8")
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)

                if msg.startswith("USERS|"):
                    users = msg.replace("USERS|", "").split(",")
                    update_users()
                else:
                    chat_history.append(msg)
                    chat_needs_update = True

        except Exception as e:
            print("RECEIVE ERROR:", e)
            break


# ---------------- DRAW ROUND RECT 
def draw_round_rect(surface, rect, color, radius=8):
    shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=radius)
    surface.blit(shape_surf, rect.topleft)


# ---------------- CREATE CHAT UI 
def create_chat_ui(WIDTH, HEIGHT):
    global chat_box, users_box, message_input, send_btn, disconnect_btn, manager

    chat_box = pygame_gui.elements.UITextBox(
        "",
        pygame.Rect(20, 20, WIDTH - 280, HEIGHT - 200),
        manager,
        object_id="#chat_box"
    )

    users_box = pygame_gui.elements.UITextBox(
        "",
        pygame.Rect(WIDTH - 250, 20, 230, HEIGHT - 200),
        manager,
        object_id="#users_box"
    )

    message_input = pygame_gui.elements.UITextEntryLine(
        pygame.Rect(20, HEIGHT - 150, WIDTH - 280, 50),
        manager
    )

    send_btn = pygame_gui.elements.UIButton(
        pygame.Rect(20, HEIGHT - 80, 200, 50),
        "SEND",
        manager
    )

    disconnect_btn = pygame_gui.elements.UIButton(
        pygame.Rect(240, HEIGHT - 80, 200, 50),
        "DISCONNECT",
        manager
    )

#-----------------
def load_account():

    if not os.path.exists(ACCOUNT_FILE):

        with open(ACCOUNT_FILE, "w") as f:
            json.dump({
                "username": "",
                "last_change": 0
            }, f)

    with open(ACCOUNT_FILE, "r") as f:
        return json.load(f)


def save_account(data):
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def can_change_name():
    account = load_account()

    last_change = account.get("last_change", 0)

    return time.time() - last_change >= NAME_CHANGE_DELAY

# ---------------- CONNECT
def connect():
    global connected, in_chat, username, client

    account = load_account()

    typed_name = login_input.get_text().strip()
    saved_name = account.get("username", "")

    username = saved_name if saved_name != "" else typed_name

    if username == "":
        return

    # REMOVE LOGIN UI
    login_input.kill()
    connect_btn.kill()
    login_quit_btn.kill()
    modify_btn.kill()

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect((HOST, PORT))
        client.sendall(f"CONNECT|{username}\n".encode("utf-8"))
        client.settimeout(None)

    except Exception as e:
        print("Connection error:", e)
        return

    connected = True
    in_chat = True

    create_chat_ui(screen.get_width(), screen.get_height())

    threading.Thread(target=receive, daemon=True).start()


# ---------------- SEND MESSAGE
def send_message():
    if not connected:
        return

    msg = message_input.get_text().strip()
    if msg == "":
        return

    try:
        client.send(f"CHAT|{username}|{msg}\n".encode("utf-8"))
        message_input.set_text("")
    except:
        pass


# ---------------- DISCONNECT
def disconnect():
    global connected, in_chat, client

    if connected:
        try:
            client.send(f"DISCONNECT|{username}\n".encode("utf-8"))
            client.close()
        except:
            pass

    connected = False
    in_chat = False

    chat_history.clear()
    users.clear()

    for ui in [chat_box, users_box, message_input, send_btn, disconnect_btn]:
        if ui:
            ui.kill()


# ---------------- LOOP
def run_chat(game_screen, WIDTH, HEIGHT):
    global manager, screen, login_input, connect_btn, login_quit_btn, modify_btn
    global connected, in_chat, info_message, chat_needs_update

    screen = game_screen

    manager = pygame_gui.UIManager(
        (WIDTH, HEIGHT),
        theme_path="network/theme.json"
    )

    # LOGIN UI
    login_input = pygame_gui.elements.UITextEntryLine(
        pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 100, 300, 50),
        manager
    )

    connect_btn = pygame_gui.elements.UIButton(
        pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 30, 300, 50),
        "CONNECT",
        manager
    )

    login_quit_btn = pygame_gui.elements.UIButton(
        pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 40, 300, 50),
        "QUIT",
        manager
    )

    modify_btn = pygame_gui.elements.UIButton(
        pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 110, 300, 50),
        "MODIFY NAME",
        manager
    )

    running = True
    disconnect_requested = False
    account = load_account()

    if account["username"] != "":
        login_input.set_text(account["username"])

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "menu"

            manager.process_events(event)

            if not in_chat:

                if event.type == pygame_gui.UI_BUTTON_PRESSED:

                    if event.ui_element == connect_btn:
                        connect()

                    if event.ui_element == login_quit_btn:
                        return "menu"

                    if event.ui_element == modify_btn:

                        account = load_account()
                        new_name = login_input.get_text().strip()

                        remaining = NAME_CHANGE_DELAY - (time.time() - account["last_change"])

                        if remaining > 0:
                            remaining = int(remaining)

                            if remaining >= 3600:
                                value = remaining // 3600
                                unit = "h"
                            elif remaining >= 60:
                                value = remaining // 60
                                unit = "min"
                            else:
                                value = remaining
                                unit = "s"

                            info_message = f"Attends {value}{unit} avant de changer de pseudo."
                            continue

                        if new_name == "":
                            info_message = "Pseudo vide interdit."
                            continue

                        account["username"] = new_name
                        account["last_change"] = time.time()
                        save_account(account)

                        username = new_name
                        info_message = "Pseudo changé avec succès."
                        continue

            else:
                if event.type == pygame_gui.UI_BUTTON_PRESSED:

                    if event.ui_element == send_btn:
                        send_message()

                    if event.ui_element == disconnect_btn:
                        disconnect_requested = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        send_message()

        manager.update(dt)
     
        screen.fill((20, 26, 35))

  
        pygame.draw.rect(
            screen,
            (31, 42, 58),
            pygame.Rect(10, 10, WIDTH - 20, HEIGHT - 20),
            border_radius=20
        )

        # ---------------- BACKGROUND ARROND
        if in_chat:

            # CHAT PANEL
            draw_round_rect(
                screen,
                pygame.Rect(23, 23, WIDTH - 285, HEIGHT - 202),
                (44, 62, 85),
                radius=16
            )

            pygame.draw.rect(
                screen,
                (102, 179, 255), 
                pygame.Rect(20, 20, WIDTH - 280, HEIGHT - 200),
                2,
                border_radius=18
            )

            # USERS PANEL
            draw_round_rect(
                screen,
                pygame.Rect(WIDTH - 250, 20, 230, HEIGHT - 200),
                (44, 62, 85),
                radius=16
            )

            pygame.draw.rect(
                screen,
                (102, 179, 255),
                pygame.Rect(WIDTH - 250, 20, 230, HEIGHT - 200),
                2,
                border_radius=18
            )


        if not in_chat and info_message != "":

            font = pygame.font.SysFont("consolas", 18, bold=True)

            text = font.render(info_message, True, (102, 179, 255))

            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 190))

            screen.blit(text, rect)

        manager.draw_ui(screen)

        pygame.display.update()

        if disconnect_requested:
            disconnect()
            return "menu"
        
        if chat_needs_update:
            update_chat()
            chat_needs_update = False

    return "menu"