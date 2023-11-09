from bitarray import bitarray
from bitarray.util import hex2ba, ba2hex, int2ba, ba2int

Filas = ['637c777bf26b6fc53001672bfed7ab76','ca82c97dfa5947f0add4a2af9ca472c0','b7fd9326363ff7cc34a5e5f171d83115','04c723c31896059a071280e2eb27b275',
'09832c1a1b6e5aa0523bd6b329e32f84','53d100ed20fcb15b6acbbe394a4c58cf','d0efaafb434d338545f9027f503c9fa8','51a3408f929d38f5bcb6da2110fff3d2',
'cd0c13ec5f974417c4a77e3d645d1973','60814fdc222a908846eeb814de5e0bdb','e0323a0a4906245cc2d3ac629195e479','e7c8376d8dd54ea96c56f4ea657aae08',
'ba78252e1ca6b4c6e8dd741f4bbd8b8a','703eb5664803f60e613557b986c11d9e','e1f8981169d98e949b1e87e9ce5528df','8ca1890dbfe6426841992d0fb054bb16']
FilasInv = ['52096ad53036a538bf40a39e81f3d7fb','7ce339829b2fff87348e4344c4dee9cb','547b9432a6c2233dee4c950b42fac34e','082ea16628d924b2765ba2496d8bd125',
'72f8f66486689816d4a45ccc5d65b692','6c704850fdedb9da5e154657a78d9d84','90d8ab008cbcd30af7e45805b8b34506','d02c1e8fca3f0f02c1afbd0301138a6b',
'3a9111414f67dcea97f2cfcef0b4e673','96ac7422e7ad3585e2f937e81c75df6e','47f11a711d29c5896fb7620eaa18be1b','fc563e4bc6d279209adbc0fe78cd5af4','1fdda8338807c731b11210592780ec5f',
'60517fa919b54a0d2de57a9f93c99cef','a0e03b4dae2af5b0c8ebbb3c83539961','172b047eba77d626e169146355210c7d']

m = bitarray(128)
    
#método principal
def cifrado(mensaje, clave):
    mensaje = padding(mensaje)
    Mensaje = bloques(mensaje)
    cifrado = ""
    for bloque in Mensaje:
        cifrado += AES(bloque, clave)
    return(cifrado)

#funcion padding para utilizar al final para rellenar
def padding(mensaje):
    m = mensaje+ '80'
    L = len(m)
    r = L%32
    if r !=0:
        m += '0' * (32-r)

def bloques(dato, k):
    return [dato[i:i+k] for i in range(0, len(dato), k)]

def AES():
    pass


#funciones de cifrado
#funcion principal
'''def AES(mensaje, clave):
    #mensaje y clave en hexadecimal
    mensaje = string2hex(mensaje)
    clave = string2hex(clave)
    #mensaje y clave en binario
    mensaje = hex2ba(mensaje)
    clave = hex2ba(clave)
    #mensaje y clave en bloques de 128 bits
    Mensaje = bloques(mensaje, 128)
    Clave = bloques(clave, 128)
    #cifrado
    cifrado = ""
    for bloque in Mensaje:
        cifrado += cifrar(bloque, Clave)
    return(cifrado)'''

def cifrar(bloque, Clave):
    pass

#-------------KEY EXPANSION----------------

def keyExpansion(clave):
    w = []
    i= 0
    while i<8:
       # w = [clave[32*i:32*i+32]] for i in range(8)]
        w.append(clave[i:i+8]) #cogemos la clave de 0 hasta 7
        i += 1
    i = 8
    while i<60:
        temp = w[i-1]
        if i % 8 == 0:
            temp = SubWord(RotWord(temp))
            temp = hex2ba(temp)
            temp ^= Rcon[i//8]
        elif i % 8 == 4:
            temp = SubWord(temp)
            temp = hex2ba(temp)
        temp = hex2ba(w[i-8]^temp)
        w.append(ba2hex(temp))
        i += 1
        return(agrupar(w,4))
    #w = ['8hex' 60 palabras]
    #w = ['32hex' 15 claves]  #devolver lista (K) con 15 claves de 128 bits (32 hexadecimales)

def SubWord(palabra):
    S = []
    for i in range(0, 8, 2):
        S.append(Sbox[palabra[i:i+2]])
    return(''.join(S))

'''
def SubWord(palabra
    W = [w[8*i : 8*i+8] for i in range(4)]
    s = [Subytes (x) for x in W] 
    return(reduce(lamda x,y: x + y, S)))
'''

def RotWord(palabra):
    return(palabra[8:]+palabra[:8])

def Rcon(i):
    R = [1]
    for j in range(1, i):
        R.append(R[j-1] << 1)
        if R[j-1] & 0x80:
            R[j] ^= 0x1b
    return(R[i-1])

def agrupar(L, k):
    n = len(L)
    assert n % k == 0
    G = []
    for i in range(0, n, k):
        G.append(pegar(L[i:+k]))
    return(G)


#-------------CIFRADO----------------

def SubBytes(estado):
    S = []
    for i in range(0, 8, 2):
        S.append(Sbox[estado[i:i+2]])
    return(''.join(S))

def ShiftRows(estado):
    E = []
    for i in range(4):
        E.append(estado[i*8:i*8+8])
    E[1] = E[1][2:]+E[1][:2]
    E[2] = E[2][4:]+E[2][:4]
    E[3] = E[3][6:]+E[3][:6]
    return(''.join(E))

def MixColumns(estado):
    E = traspuesta(estado)
    for i in range(4):
        E[i] = MixColumn(E[i])
    return(traspuesta(E))

def MixColumn(columna):
    C = trocear(columna, 2)
    C = [ba2int(x) for x in C]
    C = [x << 1 for x in C]
    C = [x ^ (x & 0x1b) for x in C]
    C = [int2ba(x, 8) for x in C]
    C = pegar(C)
    return(C)

#Devuelve la matriz traspuesta
def traspuesta(estado):
    E = []
    for i in range(4):
        E.append([x[i] for x in estado])
    return(E)

#Divide un bitarray B en trozos de tamaño k
def trocear(B, k):
    """
    Divide un bitarray B en trozos de tamaño k
    Warning: la longitud de B debe ser múltiplo de k

    Parameters
    ----------
    B : bitarray.
    k : int.

    Returns
    -------
    list de bitarrays de tamaño k.

    """
    assert type(k) == int and k > 0
    assert isinstance(B, bitarray)
    L = len(B)
    assert L % k == 0
    lista = []
    for i in range(0, L, k):
        lista.append(B[i:i+k])
    return(lista)

def AddRoundKey(estado, clave):
    return(estado^clave)





#--------------funciones utiles----------------

#convertir cadena de texto en hexadecimal
def string2hex(cadena):
    L= [ord(letra) for letra in cadena]
    H = [hex(n)[2:]for n in L] #si ponemos pej. hex(124) devuelve '0x7c' y nos interesa solo a partir del 2
    h = '"'.join(H)
    return(h)

#convertir número hexadecimal en cadena de texto
def hex2string(h):
    H = [h[i:i+2] for i in range(0, len(h), 2)]
    L = [int(x, 16) for x in H]
    Letras = [chr(n) for n in L]
    return('"'.join(L))

def pegar(L):
    from functools import reduce
    B = reduce(lambda x, y: x + y, L)
    return(B)

def Sbox(palabra):
    S = []
    for i in range(0, 8, 2):
        S.append(Sbox[palabra[i:i+2]])
    return(''.join(S))

def columnas(lista):
    estado = []
    for i in range(4):
        estado.append(lista[i:i+4])
    return(estado)






























    


