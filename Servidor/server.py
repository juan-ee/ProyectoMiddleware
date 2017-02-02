import socket
import sys
import time
import threading
import pickle
import os
import mensajeria


def escuchar(conn):
    caso=mensajeria.recibir(conn)
    if caso == 'DOWNLOAD':
        mensajeria.enviar(conn,pickle.dumps(os.listdir('Libros')))
        mensajeria.enviar_archivo(conn,'Libros/'+mensajeria.recibir(conn))        
    else:
        mensajeria.descargar_libro(conn,'Libros/'+mensajeria.recibir(conn))
    conn.close()
    return

s = socket.socket()
s.bind(('', int(sys.argv[1])))
s.listen(5)
print 'Servidor escuchando....'
n=0;
while True:
  conn, addr = s.accept()
  threading.Thread(target=escuchar,args=(conn,)).start()
  n+=1
  print n,':',addr[0]
