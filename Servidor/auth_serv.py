import pickle

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def autenticar(usuario,clave):
    try:
     return pickle.load(open('usuarios','rb'))[usuario]==clave
    except:
     return False

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(autenticar, "autenticar")
server.serve_forever()
