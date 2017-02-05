import socket
import sys
import time
import threading
import pickle
import os
import mensajeria

def autenticar(usuario,clave):
    try:
     return pickle.load(open('usuarios','rb'))[usuario]==clave
    except:
     return False

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
  credenciales=pickle.loads(mensajeria.recibir(conn))
  if(autenticar(credenciales[0],credenciales[1])):
      mensajeria.enviar(conn,'ACCEPTED')
      threading.Thread(target=escuchar,args=(conn,)).start()
  else:
      mensajeria.enviar(conn,'REJECTED')
  n+=1
  print n,':',addr[0]
