import socket
import threading
import os

def RetrFile(name, sock):
    filename = sock.recv(5120000000)
    print(filename.decode('utf-8'))
    if os.path.isfile(filename.decode('utf-8')):
        sock.send(str.encode('EXISTS '+ str(os.path.getsize(filename.decode('utf-8')))))
        userResponse = sock.recv(51200000)
        if userResponse[:2].decode('utf-8') == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(51200000)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(51200000)
                    sock.send(bytesToSend)
    else:
        sock.send(str.encode('ERR!!!'))

    sock.close()

def Main():
    host = '192.168.43.104'
    port = 5000

    s = socket.socket()
    s.bind((host,port))

    s.listen(5)

    print("Server Started.")
    while True:
        c, addr = s.accept()
        print(f"Client Connect ip:<{addr}>")
        #RetrFile('thrillee', c)
        t = threading.Thread(target=RetrFile, args=("retrThread", c))
        t.start()

    s.close()

if __name__ == '__main__':
    Main()
