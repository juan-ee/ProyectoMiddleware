import struct
import socket

def enviar(sock, data):
 length = len(data)
 sock.sendall(struct.pack('!I',length))
 sock.sendall(data)

def recibir(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def descargar_libro(s,libro):
     with open(libro, 'wb') as f:
         while 1:
             data = s.recv(1024)
             if not data:
                 break
             f.write(data)
     f.close()

def enviar_archivo(conn,filename):
  f = open(filename,'rb')
  l = f.read(1024)
  while (l):
   conn.send(l)
   l = f.read(1024)
  f.close()  
