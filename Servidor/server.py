import sys
import os
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import atexit
@atexit.register
def goodbye():
    global balanceador,server
    balanceador.quitar_servidor(server.server_address)

class Servidor(SimpleXMLRPCServer):
    def process_request(self, request, client_address):
        self.client_address = client_address
        return SimpleXMLRPCServer.process_request(self, request, client_address)

def bajar_libro(libro):
    with open('Libros/'+libro, "rb") as handle:
         return xmlrpclib.Binary(handle.read())
    handle.close()

def subir_libro(nombre,libro):
    with open('Libros/'+nombre, 'wb') as handle:
        handle.write(libro.data)
    handle.close()

def obtener_lista():
     return os.listdir('Libros')

server = Servidor(('localhost', int(sys.argv[1])),allow_none=True)
print "Back end..."
server.register_function(obtener_lista, "obtener_lista")
server.register_function(bajar_libro, "bajar_libro")
server.register_function(subir_libro, "subir_libro")

balanceador = xmlrpclib.ServerProxy("http://localhost:3000/")
balanceador.agregar_servidor(server.server_address)

server.serve_forever()
