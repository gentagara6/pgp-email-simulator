import socket
import threading
import json
import os
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000
MAILBOX_DIR = "mailboxes"

if not os.path.exists(MAILBOX_DIR):
    os.makedirs(MAILBOX_DIR)


def log(message):
    print(f"[SERVER {datetime.now().strftime('%H:%M:%S')}] {message}")


def handle_client(conn, addr):

    log(f"Client connected: {addr}")

    try:

        data = conn.recv(100000).decode()

        request = json.loads(data)

        action = request.get("action")

        if action == "send":

            sender = request["sender"]
            receiver = request["receiver"]

            email_data = {
                "sender": sender,
                "receiver": receiver,
                "package": request["package"],
                "time": str(datetime.now())
            }

            save_email(receiver, email_data)

            log(f"New encrypted email received from {sender}")
            log(f"Email forwarded to {receiver}")

            response = {
                "status": "success",
                "message": "Email sent successfully."
            }

        elif action == "receive":

            receiver = request["receiver"]

            emails = get_emails(receiver)

            log(f"{receiver} checked mailbox.")

            response = {
                "status": "success",
                "emails": emails
            }

        else:

            response = {
                "status": "error",
                "message": "Invalid action."
            }

        conn.send(json.dumps(response).encode())

    except Exception as e:

        response = {
            "status": "error",
            "message": str(e)
        }

        conn.send(json.dumps(response).encode())

    finally:
        conn.close()


def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind((HOST, PORT))

    server.listen()

    log("Email server started...")