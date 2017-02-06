import random
import sys
import xmlrpclib
import pickle
from SimpleXMLRPCServer import SimpleXMLRPCServer


def agregar_servidor(serv):
    global servidores
    servidores.append('http://'+serv[0]+':'+str(serv[1]))

def quitar_servidor(serv):
    global servidores
    servidores.remove('http://'+serv[0]+':'+str(serv[1]))

def get_servidor():
    global servidores
    return random.choice(servidores)

def autenticar(usuario,clave):
    try:
     return pickle.load(open('usuarios','rb'))[usuario]==clave
    except Exception as e:
     print e
     return False

servidores=[]
server = SimpleXMLRPCServer(("localhost", int(sys.argv[1])),allow_none=True)
print 'Front end funcionando ...'
server.register_function(agregar_servidor, "agregar_servidor")
server.register_function(quitar_servidor, "quitar_servidor")
server.register_function(autenticar, "autenticar")
server.register_function(get_servidor, "get_servidor")
server.serve_forever()
