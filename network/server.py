import socket
import threading
import json
import time
import os

HOST = "0.0.0.0"
PORT = 5555

MESSAGES_FILE = "messages.json"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# ---------------- STATE
clients = {}
users = []


# ---------------- LOAD MESSAGES
def load_messages():

    if not os.path.exists(MESSAGES_FILE):
        return []

    try:
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []


# ---------------- SAVE MESSAGES
def save_messages(messages):

    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4)


# ---------------- CLEAN OLD
def clean_old_messages():

    messages = load_messages()

    now = time.time()

    messages = [
        m for m in messages
        if now - m["time"] < 48 * 3600
    ]

    save_messages(messages)


# ---------------- SAVE ONE MESSAGE
def save_message(username, text):

    clean_old_messages()

    messages = load_messages()

    messages.append({
        "user": username,
        "text": text,
        "time": time.time()
    })

    save_messages(messages)


# ---------------- SEND HISTORY
def send_history(client):

    messages = load_messages()

    for msg in messages:
        line = f"{msg['user']}: {msg['text']}"

        try:
            client.send((line + "\n").encode("utf-8"))
        except:
            pass


# ---------------- BROADCAST
def broadcast(msg):

    dead_clients = []

    for c in clients:
        try:
            c.send((msg + "\n").encode("utf-8"))

        except:
            dead_clients.append(c)

    for c in dead_clients:
        remove_client(c)


# ---------------- USERS UPDATE
def send_users():

    msg = "USERS|" + ",".join(users)
    broadcast(msg)


# ---------------- REMOVE CLIENT
def remove_client(client):

    if client in clients:

        username = clients[client]

        if username in users:
            users.remove(username)

        del clients[client]

        if username:
            print(f"[LEAVE] {username}")

            broadcast(f"[SERVER] {username} left")
            send_users()

    try:
        client.close()
    except:
        pass


# ---------------- CLIENT HANDLER
def handle_client(client):

    buffer = ""

    try:
        while True:

            data = client.recv(1024).decode("utf-8")

            if not data:
                break

            buffer += data

            while "\n" in buffer:

                msg, buffer = buffer.split("\n", 1)

                print("RAW MSG:", msg)

                parts = msg.split("|")

                # ---------------- CONNECT
                if parts[0] == "CONNECT":

                    username = parts[1].strip()

                    # nom déjà pris
                    if username in users:

                        client.send(
                            "[SERVER] Username already taken\n".encode("utf-8")
                        )

                        client.close()
                        return

                    users.append(username)

                    clients[client] = username

                    print(f"[JOIN] {username}")
                    send_history(client)

                    broadcast(f"[SERVER] {username} joined")
                    
                    send_users()

                # ---------------- CHAT
                elif parts[0] == "CHAT":

                    username = parts[1]

                    text = "|".join(parts[2:])

                    print(f"[CHAT] {username}: {text}")

                    # save message
                    save_message(username, text)

                    # broadcast
                    broadcast(f"{username}: {text}")

                # ---------------- DISCONNECT
                elif parts[0] == "DISCONNECT":

                    raise Exception("disconnect")

    except Exception as e:

        print("CLIENT ERROR:", e)

    remove_client(client)


# ---------------- MAIN LOOP
print(f"Server running on {HOST}:{PORT}")

while True:

    client, addr = server.accept()

    clients[client] = None

    print("Client connected:", addr)

    thread = threading.Thread(
        target=handle_client,
        args=(client,)
    )

    thread.daemon = True
    thread.start()