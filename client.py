import socket

HOST = '192.168.178.109'  # IP del PC
PORT = 5000

def avvia_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(sock.recv(1024).decode())

    nome = input("Nome studente: ")
    sock.sendall(nome.encode())

    print(sock.recv(1024).decode())

    while True:
        print("\nINVIA | CODA | ESCI")
        cmd = input(">> ").upper()

        sock.sendall(cmd.encode())

        if cmd == "ESCI":
            print(sock.recv(1024).decode())
            break

        elif cmd == "CODA":
            print(sock.recv(4096).decode())

        elif cmd == "INVIA":
            print(sock.recv(1024).decode())

            sensore = input("Sensore (luce/rumore): ")
            valore = input("Valore Phyphox: ")
            luogo = input("Luogo: ")

            msg = f"{sensore}|{valore}|{luogo}"
            sock.sendall(msg.encode())

            print(sock.recv(1024).decode())

        else:
            print("Comando non valido")

    sock.close()

if __name__ == "__main__":
    avvia_client()