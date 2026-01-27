import socket

def send_move(conn, x, y):
    conn.send(f"MOVE {x} {y}".encode())

def send_doubleclick(conn, x, y):
    conn.send(f"DC {x} {y}".encode())

def start_server(host="0.0.0.0", port=9999):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print("[+] Menunggu klien...")

    conn, addr = s.accept()
    print(f"[+] Klien terhubung: {addr}")

    while True:
        try:
            data = input("(x y / dc x y / exit): ")

            if data.lower() == "exit":
                break

            parts = data.split()

            # gerak kursor
            if len(parts) == 2:
                x, y = map(int, parts)
                send_move(conn, x, y)

            # double click
            elif len(parts) == 3 and parts[0].lower() == "dc":
                x, y = map(int, parts[1:])
                send_doubleclick(conn, x, y)

        except Exception as e:
            print("Error:", e)
            break

    conn.close()
    s.close()
