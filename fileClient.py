import socket
import time

start = ''

filename = ''
def Main():
    global filename ,start
    host = '192.168.43.97'
    port = 5000

    s = socket.socket()
    s.connect((host,port))

    filename = input('Filename -> ')
    if filename != 'q':
        s.send(str.encode(filename))
        data = s.recv(5120000)
        if data[:6].decode('utf-8') == 'EXISTS':
            filesize = data[6:].decode('utf-8')
            message = input(f'The file exists. {filesize} Bytes. download? (Y/N)-> ')
            if message.lower() == "y":
                start = time.time()
                s.send(str.encode("OK"))
                f = open('new_'+filename, 'wb')
                # 50mb/sec
                data = s.recv(5120000)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < int(filesize):
                    data = s.recv(5120000*10000)
                    totalRecv += len(data)
                    f.write(data)
                    print('{}% Done'.format(round(totalRecv/int(filesize)*100, 2)))
                f.close()
                t = time.time() - start
                print(f'Download is complete! {round(t,2)} secs')
        else:
               print('File does not exist!')

    s.close()

if __name__ == '__main__':
    while filename != 'q':
        Main()

       
