import socket
import threading
import queue
import csv
import os
from datetime import datetime
 
HOST='0.0.0.0'
PORT=5000
CSV_FILE='misure.csv'
 
coda=queue.Queue()
lock=threading.Lock()
coda_visibile=[]
 
def inizializza_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE,'w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f)
            writer.writerow([
                'studente',
                'sensore',
                'valore',
                'luogo',
                'data_ora'
            ])
 
def salva_csv(riga):
    with open(CSV_FILE,'a',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(riga)
 
def gestisci_client(conn,addr):
    print(f"[CONNESSO] {addr}")
 
    try:
        conn.sendall(
            b"Benvenuto in EcoMonitor!\nInserisci il tuo nome: "
        )
 
        studente=conn.recv(1024).decode().strip()
 
        conn.sendall(
            f"Ciao {studente}! Comandi: INVIA | CODA | ESCI\n".encode()
        )
 
        while True:
            cmd=conn.recv(1024).decode().strip().upper()
 
            if not cmd:
                break
 
            if cmd=="ESCI":
                conn.sendall(b"Connessione chiusa.\n")
                break
 
            elif cmd=="CODA":
                with lock:
                    if coda_visibile:
                        stato="\n".join(
                            f"[{i+1}] {r}"
                            for i,r in enumerate(coda_visibile)
                        )
                        risposta=f"Coda attuale:\n{stato}\n"
                    else:
                        risposta="La coda e' vuota.\n"
 
                conn.sendall(risposta.encode())
 
            elif cmd=="INVIA":
                conn.sendall(
                    b"Formato: sensore|valore|luogo\n"
                )
 
                dati=conn.recv(1024).decode().strip()
 
                try:
                    sensore,valore,luogo=dati.split("|")
                    valore=float(valore)
 
                except:
                    conn.sendall(
                        b"Errore formato dati.\n"
                    )
                    continue
 
                data_ora=datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
 
                riga=[
                    studente,
                    sensore,
                    valore,
                    luogo,
                    data_ora
                ]
 
                record=",".join(map(str,riga))
 
                coda.put(record)
 
                with lock:
                    coda_visibile.append(record)
 
                salva_csv(riga)
 
                coda.get()
 
                with lock:
                    if record in coda_visibile:
                        coda_visibile.remove(record)
 
                risposta=f"Dato salvato! {data_ora}\n"
 
                conn.sendall(risposta.encode())
 
                print(f"[SALVATO] {record}")
 
            else:
                conn.sendall(
                    b"Comando non valido.\n"
                )
 
    except Exception as e:
        print(f"[ERRORE] {addr} -> {e}")
 
    finally:
        conn.close()
        print(f"[DISCONNESSO] {addr}")
 
def avvia_server():
    inizializza_csv()
 
    server=socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
 
    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
 
    server.bind((HOST,PORT))
    server.listen(10)
 
    print(f"[SERVER AVVIATO] {HOST}:{PORT}")
 
    while True:
        conn,addr=server.accept()
 
        thread=threading.Thread(
            target=gestisci_client,
            args=(conn,addr)
        )
 
        thread.start()
 
        print(
            f"[THREAD ATTIVI] {threading.active_count()-1}"
        )
 
if __name__=="__main__":
    avvia_server()