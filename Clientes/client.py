import socket
import sys
import threading
import mensajeria
import pickle
import os
import random
import xmlrpclib
from termcolor import colored

def imprimir_libros(lib):
 print '\nLISTA DE LIBROS\n'
 r=range(0,len(lib))
 print ' CODIGO | LIBRO'
 print ' --------------'
 for i in r:
  #print '   %-4d | %s' % (i,lib[i])
  print colored('   '+str(i)+'   ','blue',attrs=['bold']),'|',lib[i]

def escoger_ruta_archivo():
    while 1:
        libro=raw_input('\nEscriba la ruta: ')
        if os.path.isfile(libro):
            return libro
        print colored('\nruta incorrecta','red')

def seleccionar_libro(lib):
 r=range(0,len(lib))
 while 1:
     imprimir_libros(lib)
     try:
         n=int(raw_input('\nEscriba el codigo de un libro: '))
         if n in r: break
         raise
     except:
         print colored('\nCodigo incorrecto','red')
 return lib[n]


def conectar_ftp(serv):
    back_end = xmlrpclib.ServerProxy(serv)
    try:
        while 1:
            #print '\nMENU PRINCIPAL\n\n  1.Descargar un libro\n  2.Subir un libro'
            #caso=raw_input('\nEscriba una opcion: ')
            #caso=str(random.choice(range(1,3)))
            caso='2'
            if caso == '1':
                libro=random.choice(back_end.obtener_lista())
                with open(libro, 'wb') as handle:
                    handle.write(back_end.bajar_libro('Libros/'+libro).data)
                handle.close()
                print colored('\n'+libro+' descargado con exito','green')

                break
            elif caso == '2':
                lib='Prueba.pdf'
                #lib=escoger_ruta_archivo().split('/')[-1]
                with open(lib, "rb") as handle:
                     back_end.subir_libro(lib,xmlrpclib.Binary(handle.read()))
                handle.close()
                break
            else:
                    print colored('\nOpcion incorrecta','red')
    except Exception as e:
        print e
        print colored('\nConexion fallida','red')


def menu_cliente(n):
    front_end = xmlrpclib.ServerProxy('http://'+sys.argv[1]+':'+sys.argv[2])
    if front_end.autenticar(sys.argv[3],sys.argv[4]):
        conectar_ftp(front_end.get_servidor())
    else:
        print colored('\nAUtenticacion fallida','red')
    return

for i in range(0,1):
 threading.Thread(target=menu_cliente,args=(i,)).start()
