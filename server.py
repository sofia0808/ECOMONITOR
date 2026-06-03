import socket
import threading
import csv
import os
from datetime import datetime
from queue import Queue

HOST = "0.0.0.0"
PORT = 5000
CSV_FILE = "misure.csv"

lock = threading.Lock()
client_queue = Queue()

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["studente", "sensore", "valore", "luogo", "data_ora"])

def salva(riga):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(riga)

def recv_line(conn):
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(1)
        if not chunk:
            return None
        data += chunk
    return data.decode().strip()

def handle_client(conn, addr):
    print(f"[CONNESSO] {addr}")
    try:
        conn.sendall(b"Nome studente:\n")
        studente = recv_line(conn)
        if not studente:
            return

        conn.sendall(b"OK. Comandi: INVIA | RAPIDA | ESCI\n")

        while True:
            cmd = recv_line(conn)
            if cmd is None:
                break

            cmd = cmd.upper()

            if cmd == "ESCI":
                conn.sendall(b"BYE\n")
                break

            # Gestisce sia INVIA che il comando immediato OK della modalità rapida
            elif cmd == "INVIA" or cmd == "OK":
                conn.sendall(b"INSERISCI: sensore|valore|luogo\n")

                dati = recv_line(conn)
                if not dati:
                    continue

                try:
                    sensore, valore, luogo = dati.split("|")
                    valore = float(valore)
                except Exception:
                    conn.sendall(b"ERRORE FORMATO\n")
                    continue

                ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                riga = [studente, sensore, valore, luogo, ora]

                with lock:
                    salva(riga)

                conn.sendall(f"SALVATO {ora}\n".encode())
                print("[SALVATO]", riga)

            else:
                conn.sendall(b"COMANDO NON VALIDO\n")

    except Exception as e:
        print("[ERRORE]", e)
    finally:
        conn.close()
        print(f"[DISCONNESSO] {addr}")

def worker():
    while True:
        conn, addr = client_queue.get()
        try:
            handle_client(conn, addr)
        finally:
            client_queue.task_done()

def main():
    init_csv()

    # Avvio dei thread worker
    NUM_WORKERS = 5
    for _ in range(NUM_WORKERS):
        threading.Thread(target=worker, daemon=True).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER AVVIATO] {PORT}")

    while True:
        conn, addr = server.accept()
        client_queue.put((conn, addr))

if __name__ == "__main__":
    main()
