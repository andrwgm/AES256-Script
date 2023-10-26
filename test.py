from bitarray import bitarray

m = bitarray(128)
#prueba para ver si funciona
    
#método principal
def cifrado(mensaje, clave):
    mensaje = padding(mensaje)
    Mensaje = bloques(mensaje)
    cifrado = ""
    for bloque in Mensaje:
        cifrado += AES(bloque, clave)
    return(cifrado)

def padding():
    pass

def bloques():
    pass

def AES():
    pass