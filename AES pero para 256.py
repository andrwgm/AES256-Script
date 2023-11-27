# -*- coding: utf-8 -*-

import bitarray.util
from bitarray import bitarray
from bitarray.util import hex2ba, ba2hex, ba2int, int2ba
from functools import reduce


C = ['01000000', '02000000', '04000000', '08000000', '10000000',
     '20000000', '40000000', '80000000', '1b000000', '36000000']

C = list(map(hex2ba, C))

Tabla = []
TABLA = []
TABLAInv=[]
Filas = ['637c777bf26b6fc53001672bfed7ab76','ca82c97dfa5947f0add4a2af9ca472c0','b7fd9326363ff7cc34a5e5f171d83115','04c723c31896059a071280e2eb27b275',
'09832c1a1b6e5aa0523bd6b329e32f84','53d100ed20fcb15b6acbbe394a4c58cf','d0efaafb434d338545f9027f503c9fa8','51a3408f929d38f5bcb6da2110fff3d2',
'cd0c13ec5f974417c4a77e3d645d1973','60814fdc222a908846eeb814de5e0bdb','e0323a0a4906245cc2d3ac629195e479','e7c8376d8dd54ea96c56f4ea657aae08',
'ba78252e1ca6b4c6e8dd741f4bbd8b8a','703eb5664803f60e613557b986c11d9e','e1f8981169d98e949b1e87e9ce5528df','8ca1890dbfe6426841992d0fb054bb16']
invFilas = ['52096ad53036a538bf40a39e81f3d7fb','7ce339829b2fff87348e4344c4dee9cb','547b9432a6c2233dee4c950b42fac34e','082ea16628d924b2765ba2496d8bd125',
'72f8f66486689816d4a45ccc5d65b692','6c704850fdedb9da5e154657a78d9d84','90d8ab008cbcd30af7e45805b8b34506','d02c1e8fca3f0f02c1afbd0301138a6b',
'3a9111414f67dcea97f2cfcef0b4e673','96ac7422e7ad3585e2f937e81c75df6e','47f11a711d29c5896fb7620eaa18be1b','fc563e4bc6d279209adbc0fe78cd5af4','1fdda8338807c731b11210592780ec5f',
'60517fa919b54a0d2de57a9f93c99cef','a0e03b4dae2af5b0c8ebbb3c83539961','172b047eba77d626e169146355210c7d'] 


#programa principal que realiza el paso de codificación a decodificación
def AES(m,K):  
    Kb = K[0]   
    E = m ^ Kb
    for r in range (1, 14):
        E = Sbox(E,256,'cifrar')
        E = shiftRows(E)
        E = mixColumns(E)
        E = E^(K[r])
    E = Sbox(E,256,'cifrar')
    E = shiftRows(E)
    E = E ^ (K[14])
    E = ba2hex(E)      
    return E

#programa que realiza el paso de decodificación a codificación
def invAES(M,K):
    E = M ^ K[14]
    E = invshiftRows(E)
    E = Sbox(E,256,'descifrar')
    for r in reversed(range(1,14)):
        E = E ^ K[r]
        E = mixColumnsInv(E)
        E = invshiftRows(E)
        E = Sbox(E,256,'descifrar')
    E = E ^ K[0]
    E = ba2hex(E)
    return(E)


#Realiza un bucle llamando a las diferentes funciones hasta que devuelve la lista con las 10 claves
def expand(k):  
    K = []
    K.append(k)
    for i in range(10):
        previa = K[-1]
        Previa = trozos(previa,32)
        aux = Previa[3]
        aux = permutar(aux,8)
        aux = Sbox(aux,32,'cifrar')
        aux = aux^C[i]^Previa[0]
        L = []
        L.append(aux)
        for j in range(3):
            aux = aux ^ Previa[j+1]
            L.append(aux)
        siguiente = bitarray()
        for j in range(4):
            siguiente += L[j]
        K.append(siguiente)
    return(K)


#Concatena los resultados que devuelve y los retorna.
def sbox (b,opcion): 
    if opcion=='cifrar':
        Tabla=TABLA      
    if opcion=='descifrar':
        Tabla=TABLAInv 
    x = b[:4]
    y = b[4:]
    x = ba2int(x)
    y = ba2int(y)
    res = Tabla[x][y]
   
    res = hex2ba(res)
    return (res)


#Del mensaje E coge los 8 bits y llama a la función (sbox)
def Sbox(E,s,opcion):
    B = bitarray()
    for i in range(0,s,8):
        b = E[i:i+8]
        b = sbox(b,opcion)
        B = B + b
    return (B)


#cifrar con el método ECB
def cifrarECB(longitud,m,k):
    mensajeC = []
    
    for i in range (longitud//128):
        mensajeC.append(AES(m[i],k))
        
    return mensajeC


#descifrar con el método ECB
def invCifrarECB(longitud, m, k):
    mensajeC = []
    
    for i in range (longitud//128):
        mensajeC.append(invAES(m[i],k))
    return mensajeC


#cifrar con el método CBC
def cifrarCBC(K,iv,m,longitud):
    mensajeC = []
    MensajeFinal = []

    inicio= m[0]^iv
    mensajeC = AES(inicio,K)
    MensajeFinal.insert(0,mensajeC)
    
    for i in range (1,(longitud//128)):
        mensajeC = hex2ba(mensajeC)
        inicio=mensajeC^m[i]
        mensajeC = AES(inicio,K)
        MensajeFinal.append(mensajeC)
        
    return MensajeFinal


#Se cambian las posiciones de los elementos de las filas de la matriz
def shiftRows(E):
    E = array2mat(E) 
    R = []   
    for i in range(4):
        R.append(permutar(E[i],i)) 
    R = mat2array(R)  
    return( R ) 


#Se cambian las posiciones de los elementos de las filas de la matriz 
def invshiftRows(ES):
    ES = array2mat(ES) 
    R = []   
    for i in range(4):
        R.append(invpermutar(ES[i],i)) 
    R = mat2array(R)
    return( R )


#Coge la fila de la matriz y la desplaza circularmente a la izquierda
#La primera fila no se desplaza
def permutar(fila,k):
    assert k>=0
    res=fila.copy()  
    for i in range(k):
        res.append(res[0])
        del(res[0])
    return(res)


#Coge la fila de la matriz y la desplaza circularmente a la derecha
#La primera fila no se desplaza
def invpermutar(fila,k):
    assert k>=0
    res=fila.copy()  
    for i in range(k):
        res.insert(0,res[3])
    return(res)


#Transforma (E) a matriz, hace su transpuesta y para cada elemento llama a la función (mult)
def mixColumns(E):
    E=array2mat(E)   
    E = transpose(E)  
    R = []
    for v in E:
        w = mult(v)    
        R.append(w)
    R = transpose(R)
    R = mat2array(R)
    return(R)


#Transforma (E) a matriz, hace su transpuesta y para cada elemento llama a la función (mult)
def mixColumnsInv(E):
    E=array2mat(E)   
    E = transpose(E)  
    R = []
    for v in E:
        w = multInv(v)    
        R.append(w)
    R = transpose(R)
    R = mat2array(R)
    return(R)


#La lista B se copia en una variable (b) a la cual se le añade un cero al bitarray 
def xtime(B):
    b = B.copy()
    b.append(0)
    if b[0]==0:
        del(b[0])
    else:
        b^=bitarray('100011011')
        del(b[0])
    return(b)


#Esta lista se copia en una variable (c) la cual se multiplica usando la función “xtime()” multiplicaría el primer elemento de la fila con el primer elemento de la columna y así sucesivamente. 
def mult(C):
    c = C.copy()
    res = []
    for i in range(4):
        x = xtime(c[0]) ^ xtime(c[1]) ^ c[1] ^ c[2] ^ c[3]
        res.append(x)
        c.append(c[0])
        del(c[0])
    return (res)

#Esta lista se copia en una variable (c) la cual se multiplica usando las diferentes funciones de “mult()” (mult09(), mult0e(), mult0b(), mult0d()). 
def multInv(C):
    c = C.copy()
    res = []
    for i in range(4):
        x = mult0e(c[0]) ^ mult0b(c[1]) ^ mult0d(c[2]) ^ mult09(c[3])
        res.append(x)
        c.append(c[0])
        del(c[0])
    return (res)


def mult09(b):
    a = xtime(xtime(xtime(b)))
    return(a^b)


def mult0b(b):
    a = xtime(b)
    c = xtime(xtime(a))
    return(a^b^c)


def mult0d(b):
     a = xtime(xtime(b))
     c = xtime(a)
     return(a^b^c)


def mult0e(b):
    a = xtime(b)
    c = xtime(a)
    d = xtime(c)
    return(a^c^d)


#Divide (b) en trozos en 128 bits
def trozos(b,k):   
    L = []
    for i in range(0,128,k):
        L.append(b[i:i+k])
    return L 


#Devuelve la matriz traspuesta
def transpose(E): 
    R = []
    for i in range(4):
        col = []
        for j in range(4):
            col.append(E[j][i]) 
        R.append(col)
    return(R)


#Se crea una tabla de 16 elementos de 32 caracteres a partir de la variable filas
def CrearTabla(Filas):
    for i in range(16):
        Fila = []
        for j in range(16):
            Fila.append(Filas[i][2*j:2*j+2])
        TABLA.append(Fila)
    return(TABLA)
   
    
#Se crea una tabla de 16 elementos de 32 caracteres a partir de la variable filas
def CrearTablaInv(Filas):
    for i in range(16):
        Fila = []
        for j in range(16):
            Fila.append(Filas[i][2*j:2*j+2])
        TABLAInv.append(Fila)
    return(TABLAInv)


#Transforma la lista en un bitarray y lo retorna
def mat2array(E):
    B=bitarray()
    for j in range(4):
        for i in range(4):
            B= B+E[i][j]
    return(B)

#Transforma el bitarray en una lista y lo retorna.
def array2mat(E):
    L = []
    for i in range(0,128,8):
        L.append(E[i:i+8])
    R = []
    for i in range(4):
        fila = []
        for j in range(4):
            fila.append(L[i+4*j])
        R.append(fila)
    return(R)

#Pasar el mensaje bitarray y dividirle en trozos de 128 bits
def dividir128(E,k):
    E = hex2ba(E)
    info = [E[i:i+128] 
            
    for i in range(0, len(E), 128)]
    
    return info, k


def menu_principal():
    salir = False
    opcion = 0
    
    TABLA = CrearTabla(Filas)
     
    while not salir:
     
        print("\n1.Cifrar")
        print("2.Descifrar")
        print("3.Cifrar con CBC")
        print("4.Salir del programa")
    
        print ("Elige una opcion")
     
        opcion = pedirNumeroEntero()
     
        if opcion == 1:
            print('\n\n*********************')
            print('CIFRAR\n')
            accion1()
        elif opcion == 2:
            print('\n\n*********************')
            print('DESCIFRAR\n')
            accion2()
        elif opcion == 3:
            print('\n\n*********************')
            print('CIFRAR CON CBC\n')
            accion3()
        elif opcion == 4:
            salir = True
        else:
            print ("Introduce un numero entre 1 y 4")
     
    print ("Fin")
    
    
def pedirNumeroEntero():
 
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Introduce un numero entero: "))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')

    return num

def accion1():
    
    mensajeC=[]
    m=''
    K=''
    correcto=False
    
    K = input("Introduzca la clave en formato hexadecimal: ")
    
    while(len(K)!=32):
        K = input("Introduzca la clave en formato hexadecimal: ")
    
    K=hex2ba(K)
    K=expand(K)
    
    
    while(not correcto):
        try:
            m = input('Escriba el mensaje que desea cifrar: ')
            longitud= len(hex2ba(m))
            while(longitud<128):
                m = input('Escriba el mensaje que desea cifrar: ')
                longitud= len(hex2ba(m))
            correcto=True
        except ValueError:
            print('Error, introduce un numero hexadecimal')
    
               
    if (longitud>128):
        m,K = dividir128(m,K)
        mensajeC = cifrarECB(longitud, m, K)
        mensajeC=''.join(mensajeC)
        print('\nEl mensaje cifrado es: ', mensajeC+'\n')
        print('********************************************','\n')
    if(longitud==128):
        m=hex2ba(m)
        mensajeC = AES(m,K)
        print('\nEl mensaje cifrado es: ', mensajeC+'\n')
        print('********************************************','\n')
        
    
def accion2():
    
    TABLAInv = CrearTablaInv(invFilas)
    mensajeC=[]
    m=''
    K=''
    correcto=False
    
    K = input("Introduzca la clave en formato hexadecimal: ")
    while(len(K)!=32):
        K = input("Introduzca la clave en formato hexadecimal: ")
    
    K=hex2ba(K)
    K=expand(K)
    
    
    while(not correcto):
        try:
            m = input('Escriba el mensaje que desea cifrar: ')
            longitud= len(hex2ba(m))
            while(longitud<128):
                m = input('Escriba el mensaje que desea cifrar: ')
                longitud= len(hex2ba(m))
            correcto=True
        except ValueError:
            print('Error, introduce un numero hexadecimal')
    
  
    if (longitud>128):
        m,K= dividir128(m,K)
        mensajeC = invCifrarECB(longitud, m, K)
        mensajeC=''.join(mensajeC)     
        print('\nEl mensaje descifrado es: ', mensajeC+'\n') 
        print('********************************************','\n')
    if(longitud==128):
        m=hex2ba(m)
        mensajeC = invAES(m,K)
        print('\nEl mensaje descifrado es: ', mensajeC+'\n') 
        print('********************************************','\n')

def accion3():
    
    iv = ''
    K = ''
    MensajeFinal = []
    
    K = input("Introduzca la clave en formato hexadecimal: ")
    while(len(K)!=32):
        K = input("Introduzca la clave en formato hexadecimal: ")
    
    K=hex2ba(K)
    K=expand(K)
    
    correcto=False
    correcto2=False
    while(not correcto):
        try:
            iv = input('Escriba el vector de inicialización: ')
            longitud2=len(hex2ba(iv))
            while(longitud2!=128):
                iv = input('Escriba el vector de inicialización: ')
                longitud2=len(hex2ba(iv))
            correcto=True
        except ValueError:
            print('Error, introduce un numero hexadecimal') 
           
    while(not correcto2):
        try:
            m = input('Escriba el mensaje que desea cifrar: ')
            longitud= len(hex2ba(m))
            while(longitud<128):
                m = input('Escriba el mensaje que desea cifrar: ')
                longitud= len(hex2ba(m))
            correcto2=True
        except ValueError:
            print('Error, introduce un numero hexadecimal')
    
    
    
    iv = hex2ba(iv)
    m,K= dividir128(m,K)
    MensajeFinal = cifrarCBC(K, iv, m, longitud)
    MensajeFinal=''.join(MensajeFinal)
    print('\nEl mensaje cifrado es: ',MensajeFinal +'\n')
    print('********************************************','\n')

   
def main():
    
    print('\n************************')
    print(' BIENVENIDO AL MENÚ AES')
    print('************************','\n')
    
   
    #Llamamos al menú
    menu_principal()
        
main()
    