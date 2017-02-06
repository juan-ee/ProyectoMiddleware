import socket
import sys
import time
import threading
import pickle
import os
import mensajeria

import atexit
@atexit.register
def goodbye():
    global soc_bal
    mensajeria.enviar(soc_bal,'BYE')

def autenticar(usuario,clave):
    try:
     return pickle.load(open('usuarios','rb'))[usuario]==clave
    except:
     return False

def atender(conn,addr):
    # global clientes
    f=open('log','a')
    caso=mensajeria.recibir(conn)
    if caso == 'DOWNLOAD':
        mensajeria.enviar(conn,pickle.dumps(os.listdir('Libros')))
        l=mensajeria.recibir(conn)
        mensajeria.enviar_archivo(conn,'Libros/'+l)
        f.write('['+time.strftime('%c')+'] '+addr[0]+' downloded '+l+'\n')
    else:
        l=mensajeria.recibir(conn)
        mensajeria.descargar_libro(conn,'Libros/'+l)
        f.write('['+time.strftime('%c')+'] '+addr[0]+' uploaded '+l+'\n')
    f.close()
    conn.close()
    # clientes.remove(conn)
    return

def servir(conn,addr):
    credenciales=pickle.loads(mensajeria.recibir(conn))
    if(autenticar(credenciales[0],credenciales[1])):
        mensajeria.enviar(conn,'ACCEPTED')
        hilos.append(threading.Thread(target=atender,args=(conn,addr,)))
        hilos[-1].start()
    else:
        mensajeria.enviar(conn,'REJECTED')
hilos=[]
soc_bal= socket.socket()
s = socket.socket()
s.bind(('', int(sys.argv[1])))
s.listen(5)
try:
    print 'Servidor escuchando....'
    while True:
        conn, addr = s.accept()
        if mensajeria.recibir(conn)=='BALANCEADOR':
            soc_bal=conn
        else:
            servir(conn,addr)
except Exception as e:
    print e
    sys.exit(1)
