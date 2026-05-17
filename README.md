# Simulimi i PGP për Enkriptimin e Email-eve

## Përshkrimi i Projektit

Ky projekt paraqet një simulim të protokollit PGP (Pretty Good Privacy) për komunikim të sigurt përmes email-it.

Aplikacioni është zhvilluar në Python dhe përdor arkitekturë Client-Server.  
Qëllimi i projektit është të demonstrojë:
- gjenerimin e çelësave publikë dhe privatë,
- enkriptimin dhe dekriptimin e email-eve,
- nënshkrimet digjitale,
- verifikimin e nënshkrimeve,
- komunikimin e sigurt ndërmjet përdoruesve.

Projekti simulon mënyrën se si funksionon PGP në sistemet reale të email-it.

# Struktura e Projektit

```text
pgp-email-project/
│
├── server.py
├── client.py
├── crypto_utils.py
├── README.md
├── .gitignore
│
├── keys/
└── mailboxes/
```

# Teknologjitë e Përdorura

- Python 3
- Socket Programming
- Cryptography Library
- RSA Encryption
- Fernet Encryption
- JSON
- Multi-threading

# Funksionalitetet Kryesore

- Gjenerimi i public/private keys
- Importimi dhe eksportimi i public key
- Enkriptimi i email-eve
- Dekriptimi i email-eve
- Digital signatures
- Signature verification
- Komunikimi Client-Server
- Ruajtja e email-eve të enkriptuara
- Console interface
- Logging dhe monitoring

# Instalimi i Projektit

## 1. Klonimi i Projektit

```bash
git clone https://github.com/gentagara6/pgp-email-simulator.git
cd pgp-email-simulator
```

## 2. Instalimi i Librarive

Instalohet biblioteka `cryptography`:

```bash
pip install cryptography
```

# Udhëzimet për Ekzekutimin e Programit

## Hapi 1 — Startimi i Serverit

Hapni terminalin dhe ekzekutoni:

```bash
python server.py
```

Output i pritur:

```text
[SERVER 14:22:10] Email server started...
```

## Hapi 2 — Startimi i Client-it të Parë

Hapni një terminal tjetër:

```bash
python client.py
```

Shkruani email-in:

```text
alice@gmail.com
```

## Hapi 3 — Startimi i Client-it të Dytë

Hapni një terminal tjetër:

```bash
python client.py
```

Shkruani email-in:

```text
bob@gmail.com
```

# Procesi i Përdorimit të Programit

## 1. Gjenerimi i Çelësave

Secili përdorues duhet të gjenerojë public/private key pair.

Opsioni në menu:

```text
1.Generate key pair
```

Krijohen file-at:

```text
keys/alice@gmail.com_private.pem
keys/alice@gmail.com_public.pem
```

## 2. Eksportimi i Public Key

Përdoruesi zgjedh:

```text
2.Export public key
```

Programi shfaq public key në console.

Shembull:

```text
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----
```

## 3. Importimi i Public Key

Përdoruesi tjetër zgjedh:

```text
3.Import public key
```

Dhe bën paste public key të përdoruesit tjetër.

Public key ruhet në folderin:

```text
keys/
```

## 4. Dërgimi i Email-it të Enkriptuar

Përdoruesi zgjedh:

```text
4.Send email
```

Programi:
- krijon symmetric key,
- enkripton mesazhin,
- enkripton symmetric key me RSA,
- krijon digital signature,
- dërgon email-in te serveri.

## 5. Marrja e Email-it

Përdoruesi zgjedh:

```text
5.Receive emails
```

Programi:
- dekripton symmetric key,
- dekripton email-in,
- verifikon digital signature.

# Përshkrimi i File-ave

## server.py

Ky file implementon serverin e email-eve.

Përgjegjësitë:
- pranon lidhjet nga client-at,
- ruan email-et e enkriptuara,
- forwardon email-et,
- menaxhon kërkesat e client-ëve,
- bën logging.

Funksionet kryesore:
- `handle_client()`
- `save_email()`
- `get_emails()`
- `start_server()`

## client.py

Ky file implementon client-in dhe user interface.

Përgjegjësitë:
- shfaq menunë,
- dërgon kërkesa te serveri,
- dërgon email-e,
- pranon email-e,
- importon/exporton keys.

Funksionet kryesore:
- `menu()`
- `send_email()`
- `receive_emails()`
- `send_request()`

## crypto_utils.py

Ky file implementon të gjitha operacionet kriptografike.

Përgjegjësitë:
- gjenerimi i RSA keys,
- ngarkimi i keys,
- enkriptimi,
- dekriptimi,
- digital signatures,
- signature verification.

Funksionet kryesore:
- `generate_key_pair()`
- `load_private_key()`
- `load_public_key()`
- `encrypt_and_sign()`
- `decrypt_and_verify()`

---

# Implementimi Kriptografik

## RSA Encryption

RSA përdoret për:
- gjenerimin e public/private keys,
- enkriptimin e symmetric key,
- digital signatures.

Madhësia e key:

```text
4096-bit RSA
```

## Fernet Encryption

Fernet përdoret për enkriptimin e përmbajtjes së email-it.

Avantazhet:
- enkriptim i shpejtë,
- siguri e lartë,
- symmetric encryption.

## Hybrid Encryption

Projekti kombinon:
- RSA encryption,
- Fernet symmetric encryption.

Kjo simulon mënyrën reale të funksionimit të PGP.

---

# Logging dhe Monitoring

Serveri regjistron:
- lidhjet e client-ëve,
- email-et e pranuara,
- email-et e forwarduara.

Shembull:

```
[SERVER 15:10:20] New encrypted email received from alice@gmail.com
[SERVER 15:10:20] Email forwarded to bob@gmail.com
```

