# RAT made from fully 100% python language

* With functions such as
  > Download/Upload file command
  > 
  > Keylogging of course
  >
  > screen share/shot
  >
  > camera streaming/snap
  >
  > persistence (maintaining access)
  >
  > mic, keyboard, and cursor controller

* The required modules for the server(attacker):
  > pyaudio
  >
  > colorama (optional to use)
  >
  > pyfiglet (optional to use)
  >
  > cv2

* The required modules for the client(target):
  > cv2
  >
  > pyautogui
  >
  > pynput
  >
  > mss
  >
  > numpy

# About:
This RAT only works on windows but the server can be run on linux/windows etc. 
You can modify the code or add some new functionality, and change the language  
I cannot guarantee that this RAT is 100% FUD but due to lack of database & signature, antivirus might be taking sometimes finding it especially it's custom-made Trojan  
If you want to do a persistence or run the **target.py** on another machine that has no python, you have to compile the **target.py** into executable with pyinstaller

```bash
pip install pyinstaller
```

for CLI version or  


```bash
pip install auto-py-to-exe
```

for GUI version
