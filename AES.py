from bitarray import bitarray
from bitarray.util import hex2ba, ba2hex, int2ba, ba2int

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

def AES(m,K):
    Kb = K[0]
    E = m ^ Kb
    for r in range(1, 15):
        E = Sbox(E, 256, 'cifrar')
        E = ShiftRows(E)
        E = MixColumns(E)
        E = E^(K[r])
    E = Sbox(E, 256, 'cifrar')
    E = ShiftRows(E)
    E = E^(K[15])
    E = ba2hex(E)

    return(E)

def Sbox(palabra):
    S = []
    for i in range(0, 8, 2):
        S.append(Sbox[palabra[i:i+2]])
    return(''.join(S))

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
    return(reduce(lamda x,y:x. S)))
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



def columnas(lista):
    estado = []
    for i in range(4):
        estado.append(lista[i:i+4])
    return(estado)





#Tabla del subbytes de momento en hexadecimal
'''
    part0 = ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76']
    part1 = ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0']
    part2 = ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15']
    part3 = ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75']
    part4 = ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84']
    part5 = ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf']
    part6 = ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8']
    part7 = ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2']
    part8 = ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73']
    part9 = ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db']
    part10 = ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79']
    part11 = ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08']
    part12 = ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a']
    part13 = ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e']
    part14 = ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df']
    part15 = ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']

'''