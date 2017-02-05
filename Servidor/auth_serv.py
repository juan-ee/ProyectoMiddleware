import pickle
import sys
ejm1=('us1','us1')
ejm2=('s','sd')

#with open('Usuarios/base','rb') as f:
# print pickle.load(f)
try:
 if pickle.load(open('Usuarios/base','rb'))[sys.argv[1]]==sys.argv[2]:
  print 'vale'
 else:
  raise
except:
 print 'auth failed'
 
  
