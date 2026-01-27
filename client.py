import socket
import pyautogui

def start_client(host, port=9999):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("[+] Terhubung ke server")

    while True:
        data = s.recv(1024).decode()
        if not data:
            break

        parts = data.split()

        if parts[0] == "MOVE":
            x, y = map(int, parts[1:])
            pyautogui.moveTo(x, y, duration=0.3)

        elif parts[0] == "DC":
            x, y = map(int, parts[1:])
            pyautogui.moveTo(x, y)
            pyautogui.doubleClick()


