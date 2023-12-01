import bitarray.util
from bitarray import bitarray
from bitarray.util import hex2ba, ba2hex, ba2int, int2ba

# el estado es donde se va guardando el cifrado
state = [[0 for x in range(4)] for y in range(4)]

# ten cuidado por si deja el primero como 1000... en vez de 0100...
Rcon = ['01000000', '02000000', '04000000', '08000000',
        '10000000', '20000000', '40000000', '80000000',
        '1B000000', '36000000', '6C000000', 'D8000000',
        'AB000000', '4D000000']
Rcon = [hex2ba(x) for x in Rcon]

SboxTable = [['63','7c','77','7b','f2','6b','6f','c5','30','01','67','2b','fe','d7','ab','76'],
            ['ca','82','c9','7d','fa','59','47','f0','ad','d4','a2','af','9c','a4','72','c0'],
            ['b7','fd','93','26','36','3f','f7','cc','34','a5','e5','f1','71','d8','31','15'],
            ['04','c7','23','c3','18','96','05','9a','07','12','80','e2','eb','27','b2','75'],
            ['09','83','2c','1a','1b','6e','5a','a0','52','3b','d6','b3','29','e3','2f','84'],
            ['53','d1','00','ed','20','fc','b1','5b','6a','cb','be','39','4a','4c','58','cf'],
            ['d0','ef','aa','fb','43','4d','33','85','45','f9','02','7f','50','3c','9f','a8'],
            ['51','a3','40','8f','92','9d','38','f5','bc','b6','da','21','10','ff','f3','d2'],
            ['cd','0c','13','ec','5f','97','44','17','c4','a7','7e','3d','64','5d','19','73'],
            ['60','81','4f','dc','22','2a','90','88','46','ee','b8','14','de','5e','0b','db'],
            ['e0','32','3a','0a','49','06','24','5c','c2','d3','ac','62','91','95','e4','79'],
            ['e7','c8','37','6d','8d','d5','4e','a9','6c','56','f4','ea','65','7a','ae','08'],
            ['ba','78','25','2e','1c','a6','b4','c6','e8','dd','74','1f','4b','bd','8b','8a'],
            ['70','3e','b5','66','48','03','f6','0e','61','35','57','b9','86','c1','1d','9e'],
            ['e1','f8','98','11','69','d9','8e','94','9b','1e','87','e9','ce','55','28','df'],
            ['8c','a1','89','0d','bf','e6','42','68','41','99','2d','0f','b0','54','bb','16']]

invSboxTable = [['52','09','6a','d5','30','36','a5','38','bf','40','a3','9e','81','f3','d7','fb'],
                ['7c','e3','39','82','9b','2f','ff','87','34','8e','43','44','c4','de','e9','cb'],
                ['54','7b','94','32','a6','c2','23','3d','ee','4c','95','0b','42','fa','c3','4e'],
                ['08','2e','a1','66','28','d9','24','b2','76','5b','a2','49','6d','8b','d1','25'],
                ['72','f8','f6','64','86','68','98','16','d4','a4','5c','cc','5d','65','b6','92'],
                ['6c','70','48','50','fd','ed','b9','da','5e','15','46','57','a7','8d','9d','84'],
                ['90','d8','ab','00','8c','bc','d3','0a','f7','e4','58','05','b8','b3','45','06'],
                ['d0','2c','1e','8f','ca','3f','0f','02','c1','af','bd','03','01','13','8a','6b'],
                ['3a','91','11','41','4f','67','dc','ea','97','f2','cf','ce','f0','b4','e6','73'],
                ['96','ac','74','22','e7','ad','35','85','e2','f9','37','e8','1c','75','df','6e'],
                ['47','f1','1a','71','1d','29','c5','89','6f','b7','62','0e','aa','18','be','1b'],
                ['fc','56','3e','4b','c6','d2','79','20','9a','db','c0','fe','78','cd','5a','f4'],
                ['1f','dd','a8','33','88','07','c7','31','b1','12','10','59','27','80','ec','5f'],
                ['60','51','7f','a9','19','b5','4a','0d','2d','e5','7a','9f','93','c9','9c','ef'],
                ['a0','e0','3b','4d','ae','2a','f5','b0','c8','eb','bb','3c','83','53','99','61'],
                ['17','2b','04','7e','ba','77','d6','26','e1','69','14','63','55','21','0c','7d']]

#key = hex2ba(key) y su len = 256 en binario y 64 en hex

def setState(mensaje):
    for i in range(0, 16):
        state[i % 4][i // 4] = mensaje[i*2:i*2+2]

def resetState():
    for i in range(0, 16):
        state[i % 4][i // 4] = '00'

def state2string():
    m = ''
    for i in range(0, 16):
        m += state[i % 4][i // 4]
    return(m)

# esta funcion se utiliza para juntar de 4 en 4 palabras como
# unicas entradas de un array, es decir, si antes tenias 8 palabras, 
# ahora tienes dos posiciones de array, con 4 palabras cada una.

def agrupar(L, k):
    from functools import reduce
    assert len(L) % k == 0
    N = len(L) // k
    G = [L[k*i:k*i+k] for i in range(N)]
    return(reduce(lambda x, y: x + y, w) for w in G)


# sbox coge un bitarray de 8 bits y le aplica tabla de sustitucion
def sbox(b):
    x = b[:4]
    y = b[4:]
    x = ba2int(x)
    y = ba2int(y)

    val = SboxTable[x][y]
    val = hex2ba(val)
    return (val)


# Sbox coge la palabra de 32 digitos binarios que le proporciona el 
# hex2ba(word) del return de SubWord y le aplica sbox a cada trozo de 8 bits 
# de la palabra, devolviendo un bitarray de 32 bits que son los 4 trozos de 8 
# pasados por sbox
def Sbox(word):
    B = bitarray() 
    for i in range(0,len(word),8):
        b = word[i:i+8]
        b = sbox(b)
        B = B + b
    
    #print('afterSubWord: ',ba2hex(B))
    return (B)

# RotWord es coge los dos primeros caracteres y les pone al final de la palabra
def RotWord(word): # word en hexadecimal
    # rotamos los 4 ultimos caracteres de la palabra
    return(word[8:]+word[:8])

# SubWord is a function that takes a four-byte input word and applies
# the S-box (Sec. 5.1.1,Fig. 7) to each of the four bytes to produce an output word
def SubWord(word): # word entra en hexadecimal
    #print('rotword: ',ba2hex(word))
    return Sbox(word) # y retorna el bitarray que salga de Sbox

# Nb = 4 Nk = 8 Nr = 14       Nb * (Nr + 1) = 60
def KeyExpansion(key): # key en hexadecimal
    key = hex2ba(key) # key en binario
    w = []

    # dividimos en palabras de 32 bits
    w = [key[32*i:32*i+32] for i in range(8)]

    i = 8 #Nk

    # aqui w es una lista de 8 palabras de 32 bits cada una
    # en cada iteracion se añade una nueva palabra al final de la lista w
    while i<60: # Nb * (Nr + 1)
        temp = w[i-1] # temp es un trozo de 8 caracteres
        #print('-----------Nueva iteracion-----------')
        #print('i: ',i,'temp: ', ba2hex(temp))
        if i % 8 == 0:
            temp = SubWord(RotWord(temp)) # a subWord le entran hexadecimales
            #print('Rcon: ', ba2hex(Rcon[i//8 - 1]))
            temp ^= Rcon[i//8 - 1]
            #print('temp: ',ba2hex(temp))

        elif i%8 == 4:
            temp = SubWord(temp)

        #print('w[i-8]: ',ba2hex(w[i-8]))
        temp = w[i-8]^temp

        #print('temp: ',ba2hex(temp))
        w.append(temp)

        i += 1

    return(agrupar(w,4))
    #w = ['8hex' 60 palabras]
    #w = ['32hex' 15 claves]  #devolver lista (K) con 15 claves de 128 bits (32 hexadecimales)



# Nb = 4
# -> In the AddRoundKey() transformation, a Round Key is added to the State by a simple bitwise
# XOR operation. Each Round Key consists of Nb words from the key schedule (described in Sec.
# 5.2). Those Nb words are each added into the columns of the State
# -> aqui rellenamos el estado haciendo un XOR del propio estado con 4 palabras de la key schedule
# que se calcula en el keyExpansion
def AddRoundKey(key, round):    
    #state ya tendria que estar con el valor del mensaje

    # keySchedule es una lista de 15 palabras de 128 bits cada una
    keySchedule = list(KeyExpansion(key))

    # keyScheduleYaPartido es una lista de 15 listas de 4 palabras de 32 bits cada una, es decir,
    # así podemos aplicar el XOR de cada lista de la keyScheduleYaPartida con cada fila del state,
    # que ambas tienen 4 elementos
    keyScheduleYaPartido = []
    for palabra in keySchedule:
        keySchedulePartes = [['','','',''],['','','',''],['','','',''],['','','','']]
        palabraAux = ba2hex(palabra)
        for i in range(0, 16):
            aux2 = palabraAux[2*i:2*i+2]
            keySchedulePartes[i % 4][i // 4] = aux2 # así, para cada iteracion del for, se llena cada casilla de la matrix 4x4 de manera vertical
        keyScheduleYaPartido.append(keySchedulePartes)
    
    # aplicamos el XOR
    for i in range(0, 16):
            state[i % 4][i // 4] = ba2hex(hex2ba(state[i % 4][i // 4]) ^ hex2ba(keyScheduleYaPartido[round][i % 4][i // 4]))

def subBytes():
    for i in range(0, 16):
            state[i % 4][i // 4] = ba2hex(sbox(hex2ba(state[i % 4][i // 4])))

def shiftRows():
    for i in range(0, 4):
        state[i] = state[i][i:] + state[i][:i]

def traspuesta(matrix):
    E = []
    for i in range(0, 4):
        E.append([matrix[j][i] for j in range(0, 4)])
    return(E)

# Se calcula la x multiplicacion por el binario
def xtime(B):
    b = B.copy()
    b.append(0) 
    if b[0]==0:
        del(b[0])
    else:
        b^=bitarray('100011011') # polinomio de reduccion de Rijndael
        del(b[0])
    return(b)

def multRijndael(fila): #ahora son filas porque esta traspuesta, pero realmente son columnas
    aux = []
    for i in range(4):
        x = ba2hex(xtime(hex2ba(fila[0])) ^ xtime(hex2ba(fila[1])) ^ hex2ba(fila[1]) ^ hex2ba(fila[2]) ^ hex2ba(fila[3]))
        aux.append(x)
        fila.append(fila[0])
        del(fila[0])
    return (aux)

def mixColumns():
    global state

    state = traspuesta(state)   

    for i in range(4):
        state[i] = multRijndael(state[i])
    
    state = traspuesta(state)

    return(state)












def invShiftRows():
    for i in range(0, 4):
        state[i] = state[i][-i:] + state[i][:-i]

# sbox coge un bitarray de 8 bits y le aplica tabla de sustitucion
def invsbox(b):
    x = b[:4]
    y = b[4:]
    x = ba2int(x)
    y = ba2int(y)

    val = invSboxTable[x][y]
    val = hex2ba(val)
    return (val)

def invSubBytes():
    for i in range(0, 16):
            state[i % 4][i // 4] = ba2hex(invsbox(hex2ba(state[i % 4][i // 4])))

def tresXtime(b):
    return(xtime(xtime(xtime(b))))

def mult09(b):
    return(tresXtime(b)^b)

def mult0b(b):
    return(tresXtime(b)^xtime(b)^b)


def mult0d(b):
     return(tresXtime(b)^xtime(xtime(b))^b)

def mult0e(b):
     return(tresXtime(b)^xtime(xtime(b))^xtime(b))

def invMultRijndael(fila): #ahora son filas porque esta traspuesta, pero realmente son columnas
    aux = []
    for i in range(4):
        x = ba2hex(mult0e(hex2ba(fila[0])) ^ mult0b(hex2ba(fila[1])) ^ mult0d(hex2ba(fila[2])) ^ mult09(hex2ba(fila[3])))
        aux.append(x)
        fila.append(fila[0])
        del(fila[0])
    return (aux)

def invMixColumns():
    global state

    state = traspuesta(state)   

    for i in range(4):
        state[i] = invMultRijndael(state[i])
    
    state = traspuesta(state)

    return(state)













# key en hexadecimal y mensaje en 
def cifrado(key, mensaje):

    global state

    setState(mensaje)

    #print('State init:', state2string())

    AddRoundKey(key, 0)
    

    for i in range(1, 14):
        #print('State start en round:', i, state2string())
        subBytes()
        shiftRows()
        mixColumns()
        AddRoundKey(key, i)
    
    #print('State start en round 14:', state2string())
    subBytes()
    shiftRows()
    AddRoundKey(key, 14)

def descifrado(key, mensaje):

    global state

    setState(mensaje)

    print('State init:', state2string())

    AddRoundKey(key, 14)

    for i in range(1, 14):
        print('State start en round:', i, state2string())
        invShiftRows()
        invSubBytes()
        AddRoundKey(key, i)
        invMixColumns()
    
    print('State start en round 14:', state2string())
    invShiftRows()
    invSubBytes()
    AddRoundKey(key, 0)












def menu_principal():
    exit = False
    opt = 0
     
    while not exit:
     
        print("\n1.Cifrar")
        print("2.Descifrar")
        print("0.Salir")
     
        opt = solicitarOpcion()
     
        if opt == 1:
            print('\n')
            print('    CIFRAR')
            print('~~~~~~~~~~~~~~~~')
            opt1()
        elif opt == 2:
            print('\n')
            print('    DESCIFRAR')
            print('~~~~~~~~~~~~~~~~')
            opt2()
        elif opt == 0:
            exit = True
        else:
            print ("Introduce un numero entre 1 y 2.")
            print ("Introduce 0 para salir.")
     
    print ("Exit")
    
    
def solicitarOpcion():
 
    valido=False
    numEnt=0
    while(not valido):
        try:
            numEnt = int(input("\nElija una opción: "))
            valido=True
        except ValueError:
            print('Error, debe ser un número entero (0-2)')

    return numEnt

def opt1():
    
    mensajeC=''
    mensaje=''
    key=''
    valido=False
    
    key = input("Introduzca la clave en formato hexadecimal: ")
    
    while(len(key)!=64):
        key = input("Introduzca la clave en formato hexadecimal: ")    
    
    while(not valido):
        try:
            mensaje = input('Escriba el mensaje que desea cifrar: ')
            longitud= len(hex2ba(mensaje))
            while(longitud<128):
                mensaje = input('Escriba el mensaje que desea cifrar: ')
                longitud= len(hex2ba(mensaje))
            valido=True
        except ValueError:
            print('Error, introduce el mensaje en hexadecimal')
               
    if(len(hex2ba(mensaje))==128):
        cifrado(key,mensaje)
        mensajeC = state2string()
        print('\nEl mensaje cifrado es: ', mensajeC+'\n')
        resetState()

def opt2():
    
    mensajeD=''
    mensaje=''
    key=''
    valido=False
    
    key = input("Introduzca la clave en formato hexadecimal: ")
    
    while(len(key)!=64):
        key = input("Introduzca la clave en formato hexadecimal: ")
    
    
    while(not valido):
        try:
            mensaje = input('Escriba el mensaje que desea descifrar: ')
            longitud= len(hex2ba(mensaje))
            while(longitud<128):
                mensaje = input('Escriba el mensaje que desea descifrar: ')
                longitud= len(hex2ba(mensaje))
            valido=True
        except ValueError:
            print('Error, introduce el mensaje en hexadecimal')
    
  
    if(len(hex2ba(mensaje))==128):
        descifrado(key, mensaje)
        mensajeD = state2string()
        print('\nEl mensaje descifrado es: ', mensajeD+'\n')
        resetState()

def main():
    
    print('\n~~~~~~~~~~~~~~~~')
    print('    MENÚ AES')
    print('~~~~~~~~~~~~~~~~')
    
   
    #Llamamos al menú
    menu_principal()
        
main()