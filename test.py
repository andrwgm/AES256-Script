from bitarray import bitarray

m = bitarray(128)
    
#método principal
def cifrado(mensaje, clave):
    mensaje = padding(mensaje)
    Mensaje = bloques(mensaje)
    cifrado = ""
    for bloque in Mensaje:
        cifrado += AES(bloque, clave)
    return(cifrado)

#funciones pequeñas

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

def keyExpansion(clave):
    W = []
    i= 0
    while i<8:
        w.append(clave[i:i+8]) #cogemos la clave de 0 hasta 7
        i += 1
    i = 8
    while i<60:
        temp = w[i-1]
        if i % 8 == 0:
            temp = SubWord(RotWord(temp))
            temp = hex2ba(temp)
            temp ^= Rcon[i//8]
        elif i%8 == 4:
            temp = SubWord(temp)
            temp = hex2ba(temp)
        temp = hex2ba(w[i-8])^temp
        w.append(ba2hex(temp))
        i += 1
        #return(agrupar(w,4))
    #w = ['8hex' 60 palabras]
    #w = ['32hex' 15 claves]  #devolver lista (K) con 15 claves de 128 bits (32 hexadecimales)

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

#Devuelve la matriz traspuesta
def traspuesta(estado):
    E = []
    for i in range(4):
        E.append([x[i] for x in estado])
    return(E)

def bloques(dato, k):
    return [dato[i:i+k] for i in range(0, len(dato), k)]

def columnas(lista):
    estado = []
    for i in range(4):
        estado.append(lista[i:i+4])
    return(estado)

def AES():
    pass

def padding():
    pass

def pegar(L):
    from functools import reduce
    B = reduce(lambda x, y: x + y, L)
    return(B)
    
def agrupar(L, k):
    n = len(L)
    assert n % k == 0
    G = []
    for i in range(0, n, k):
        G.append(pegar(L[i:+k]))
    return(G)

#funcion padding para utilizar al final para rellenar
def padding(mensaje):
    m = mensaje+ '80'
    L = len(m)
    r = L%32
    if r !=0:
        m += '0' * (32-r)