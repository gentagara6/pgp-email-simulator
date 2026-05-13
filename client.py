import socket
import json

from crypto_utils import(
    generate_key_pair,
    encrypt_and_sign,
    decrypt_and_verify
)

HOST = "127.0.0.1"
PORT = 5000

def export_public_key(email):
    with open(
        f"keys/{email}_public.pem",
        "r"
    ) as f:

        print("\n----- PUBLIC KEY -----")
        print(f.read())

def import_public_key(email):
    print(
        "Paste the public key. Write END when finished: "
    )

    lines = []
    while True:
        line = input()

        if line == "END":
            break

        lines.append(line)
    key_data = "\n".join(lines)

    with open(
        f"keys/{email}_public.pem",
        "w"
    ) as f:
        f.write(key_data)

    print(
        "Public key imported successfully."
    )

def send_request(request):
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    client.connect((HOST, PORT))

    client.send(
        json.dumps(request).encode()
    )

    response = client.recv(
        100000
    ).decode()

    client.close()
    return json.loads(response)

def send_email(my_email):
    receiver = input(
        "Receiver email: "
    )

    message = input(
        "Message: "
    )

    package = encrypt_and_sign(
        message,
        my_email,
        receiver
    )

    request = {
        "action": "send",
        "sender": my_email,
        "receiver": receiver,
        "package": package
    }

    response = send_request(
        request
    )

    print(
        response["message"]
    )

def receive_emails(my_email):
    request = {
        "action": "receive",
        "receiver": my_email
    }

    response = send_request(
        request
    )
    emails = response["emails"]

    if len(emails) == 0:
        print("No new emails.")
        return
    
    for email in emails:
        sender = email["sender"]

        message = decrypt_and_verify(
            email["package"],
            my_email,
            sender
        )
        print("\nFROM:", sender)
        print("MESSAGE:", message)

def menu():
    print(
        "Welcome to the PGP Email Client!"
    )

    my_email = input(
        "Enter your email: "
    )

    while True:
        print("\n===== MENU =====")

        print(
            "1.Generate key pair"
        )
        print(
            "2.Export public key"
        )
        print(
            "3.Import public key"
        )
        print(
            "4.Send email"
        )
        print(
            "5.Receive emails"
        )
        print(
            "6.Exit"
        )
        choice = input(
            "Choose: "
        )

        if choice == "1":
            generate_key_pair(
                my_email
            )
        elif choice == "2":
            export_public_key(
                my_email
            )
        elif choice == "3":
            other_email = input(
                "Owner email: "
            )
            import_public_key(
                other_email
            )
        elif choice == "4":
            send_email(
                my_email
            )
        elif choice == "5":
            receive_emails(
                my_email
            )
        elif choice == "6":
            break
        else:
            print(
                "Invalid option."
            )
menu()