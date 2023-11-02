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

def bloques():
    pass

def AES():
    pass