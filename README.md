# RAT made from fully 100% python language

* With functions such as
  > Download/Upload file command (Download only up to 3,5mb)
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

About:
 - This RAT only works on windows but the server can be run on linux/windows etc.
 - due to lack of resources & i'm a bit forking others do, it's features doesn't seem so stable, there's many bugs that i still working to fix it:
 - 1. Download error
   2. Can't start the camera more than 1x
   3. Can't screen share more than 1x
   4. When you do persistence, the input won't showing up again

 - You can modify the code/add some new functionality, and change the language
 - I cannot guarantee that this RAT is 100% FUD but due
 - to lack of database & signature, antivirus might be taking a bit of time finding it especially it's custom-made Trojan
