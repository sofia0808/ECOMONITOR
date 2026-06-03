import socket
import requests
import sys
import time

HOST = '127.0.0.1' # Modifica con l'IP del tuo server se necessario
PORT = 5000
SENSORI = ['luce', 'rumore']

def leggi_da_phyphox(ip_phyphox, sensore):
    try:
        if sensore == 'luce':
            url = f"http://{ip_phyphox}:8080/get?illum"
            chiave = "illum"
        elif sensore == 'rumore':
            url = f"http://{ip_phyphox}:8080/get?dB"
            chiave = "dB"
        else:
            return None

        risposta = requests.get(url, timeout=2)
        dati = risposta.json()
        buf = dati.get("buffer", {}).get(chiave, None)

        if isinstance(buf, dict) and "buffer" in buf:
            valori = buf["buffer"]
            if valori: return valori[-1]
        if isinstance(buf, list) and buf:
            return buf[-1]
    except Exception:
        pass
    return None

def scegli_sensore():
    print("\nSensori disponibili:")
    for i, s in enumerate(SENSORI, 1):
        print(f"  {i}. {s}")
    while True:
        scelta = input("Scegli sensore (numero): ").strip()
        if scelta.isdigit() and 1 <= int(scelta) <= len(SENSORI):
            return SENSORI[int(scelta) - 1]
        print("Scelta non valida.")

def modalita_rapida(sock, nome, sensore, luogo, ip_phyphox):
    print("\n" + "=" * 45)
    print("  MODALITA' REGISTRAZIONE RAPIDA")
    print(f"  Sensore  : {sensore} | Luogo: {luogo}")
    print("  Scrivi 'ok' (o premi INVIO) per registrare la misura.")
    print("  Scrivi 'stop' per uscire.")
    print("=" * 45 + "\n")

    contatore = 0

    while True:
        comando_utente = input("Dispositivo pronto >> ").strip().lower()

        if comando_utente == 'stop':
            print(f"\nUscita. Misure registrate in questa sessione: {contatore}")
            break

        # Se digita 'ok' oppure preme semplicemente INVIO a vuoto
        if comando_utente == 'ok' or comando_utente == '':
            valore = None
            if ip_phyphox:
                print("Lettura da Phyphox...", end="", flush=True)
                for _ in range(10):
                    valore = leggi_da_phyphox(ip_phyphox, sensore)
                    if valore is not None:
                        break
                    time.sleep(0.1)
                
            if valore is None:
                if ip_phyphox: print(" Non risponde.")
                valore_str = input("Inserisci valore manuale: ").strip()
                try:
                    float(valore_str)
                except ValueError:
                    print("Valore non valido. Misura annullata.")
                    continue
            else:
                print(f" Letto: {valore}")
                valore_str = str(valore)

            # Comunica al server l'intenzione di inserire dati rapida
            sock.sendall(b"OK\n")
            sock.recv(1024) # Scarta il prompt di sblocco del server ("INSERISCI:...")

            # Invia la stringa formattata dei dati
            sock.sendall(f"{sensore}|{valore_str}|{luogo}\n".encode())
            risposta_server = sock.recv(1024).decode().strip()

            contatore += 1
            print(f"  [{contatore}] Registrato! Risposta server: {risposta_server}\n")
        else:
            print("Comando non riconosciuto. Scrivi 'ok', premi INVIO o scrivi 'stop'.")

def avvia_client():
    print("=" * 45)
    print("  EcoMonitor - Client")
    print("=" * 45)

    ip_phyphox = input("IP phyphox (vuoto = solo manuale): ").strip()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"\n[ERRORE] Impossibile connettersi a {HOST}:{PORT}")
        return

    try:
        print("\n" + sock.recv(1024).decode(), end='')
        nome = input().strip()
        while not nome:
            nome = input("Il nome non può essere vuoto: ").strip()
        
        sock.sendall(f"{nome}\n".encode())
        print(sock.recv(1024).decode(), end='')

        while True:
            print("\nScegli modalità: RAPIDA | INVIA | ESCI")
            cmd = input(">> ").strip().upper()

            if cmd == 'ESCI':
                sock.sendall(b'ESCI\n')
                print(sock.recv(1024).decode())
                break

            elif cmd == 'RAPIDA':
                sensore = scegli_sensore()
                luogo = input("Luogo (es. laboratorio_1): ").strip()
                if not luogo:
                    print("Luogo obbligatorio.")
                    continue
                modalita_rapida(sock, nome, sensore, luogo, ip_phyphox)

            elif cmd == 'INVIA':
                # Vecchia modalità classica (una misura singola per volta richiedendo tutto)
                sock.sendall(b'INVIA\n')
                sock.recv(1024)
                sensore = scegli_sensore()
                luogo = input("Luogo: ").strip()
                valore_str = input("Valore: ").strip()
                sock.sendall(f"{sensore}|{valore_str}|{luogo}\n".encode())
                print(sock.recv(1024).decode())

    except (ConnectionResetError, BrokenPipeError):
        print("\n[ERRORE] Connessione con il server interrotta.")
    finally:
        sock.close()

if __name__ == '__main__':
    avvia_client()
