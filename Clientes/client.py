import socket
import sys
import threading
import mensajeria
import pickle
import os
import random
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

def conectar_ftp(serv,n):
    try:
        s = socket.socket()
        s.connect(serv)
        mensajeria.enviar(s,'CLIENTE')
        mensajeria.enviar(s,pickle.dumps((sys.argv[4],sys.argv[5])))
        if mensajeria.recibir(s)=='ACCEPTED':
            while 1:
                #print '\nMENU PRINCIPAL\n\n  1.Descargar un libro\n  2.Subir un libro'
                #caso=raw_input('\nEscriba una opcion: ')
                caso=str(random.choice(range(1,3)))
                if caso == '1':
                    #descargar un libro
                    mensajeria.enviar(s,'DOWNLOAD')
                    #libro=seleccionar_libro(pickle.loads(mensajeria.recibir(s)))
                    libro=random.choice(pickle.loads(mensajeria.recibir(s)))
                    mensajeria.enviar(s,libro)
                    #mensajeria.descargar_libro(s,libro)
                    mensajeria.descargar_libro(s,sys.argv[3]+'/'+libro+'.'+str(n))
                    print colored('\n'+libro+' descargado con exito','green')
                    break
                elif caso == '2':
                    #subir un libro
                    mensajeria.enviar(s,'UPLOAD')
                    #ruta=escoger_ruta_archivo()
                    #mensajeria.enviar(s,ruta.split('/')[-1])
                    mensajeria.enviar(s,'Prueba.pdf')
                    #mensajeria.enviar_archivo(s,ruta)
                    mensajeria.enviar_archivo(s,'Prueba.pdf')
                    print colored('\nlibro subido con exito','green')
                    break
                else:
                    print colored('\nOpcion incorrecta','red')
            s.close()
        else:
            print colored('\nError de autenticacion','red')
    except:
        print colored('\nConexion fallida','red')
        s.close()


def menu_cliente(n):
    s = socket.socket()
    s.connect((sys.argv[1], int(sys.argv[2])))
    serv=pickle.loads(mensajeria.recibir(s))
    s.close()
    conectar_ftp(serv,n)



for i in range(0,100):
 threading.Thread(target=menu_cliente,args=(i,)).start()
