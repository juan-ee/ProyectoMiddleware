from collections import deque
import socket
import sys
import time
import threading
import pickle
import random
import mensajeria

class Balanceador(object):
 def __init__(self):
  #self.cola=deque()
  self.cluster=[]
  #conexion con todos los servidores
  self.conectar_servidores()
  #inicio servidor
  threading.Thread(target=self.f_servidor).start()
  #inicio de la funcion del balanceador
  #threading.Thread(target=self.balanceador).start()


 def conectar_servidores(self):
  for i in range(3,len(sys.argv)):
   c = socket.socket()
   c.connect((sys.argv[2],int(sys.argv[i])))
   mensajeria.enviar(c,'BALANCEADOR')
   self.cluster.append(c)
   threading.Thread(target=self.f_cliente,args=(c,)).start()

 def f_servidor(self):
  s=socket.socket()
  s.bind(('',int(sys.argv[1])))
  s.listen(5)
  n=0;
  while 1:
   conn, addr = s.accept()
   n+=1
   print n
   if len(self.cluster)==0:break #se detiene si ya no hay mas servidores que atiendan
   mensajeria.enviar(conn,pickle.dumps(random.choice(self.cluster).getpeername()))
   conn.close()
  s.close()
  return

 def f_cliente(self,socket):
     try:
         if (mensajeria.recibir(socket)):
             raise
     except:
         socket.close()
         self.cluster.remove(socket)
     return

Balanceador()
