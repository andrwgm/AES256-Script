import bitarray.util
from bitarray import bitarray
from bitarray.util import hex2ba, ba2hex, ba2int, int2ba

# ------ VARIABLES GLOBALES Y FUNCIONALIDADES GENÉRICAS ------

# Inicializamos la matriz que guardará el estado del cifrado
state = [[0 for x in range(4)] for y in range(4)]

# Establecemos los valores de Rcon y les transformamos a binario para su
# posterior uso
Rcon = ['01000000', '02000000', '04000000', '08000000',
        '10000000', '20000000', '40000000', '80000000',
        '1B000000', '36000000', '6C000000', 'D8000000',
        'AB000000', '4D000000']
Rcon = [hex2ba(x) for x in Rcon]

# Establecemos las tablas de valores de sustitución que se usan en la
# funcion Sbox (cifrado y descifrado)
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

# Declaramos algunas funciones que nos serán útiles para manejar el
#estado de los cifrados y su traducción de matrices a strings

def setState(mensaje):
    """
    Input: mensaje en hexadecimal
    Output: state (matriz 4x4) con el mensaje en hexadecimal

    Esta funcion se encarga de coger el mensaje en hexadecimal y
    pasarlo a la matriz state, que es la que se utiliza para almacenar
    el estado del cifrado AES
    """
    for i in range(0, 16):
        state[i % 4][i // 4] = mensaje[i*2:i*2+2]

def resetState():
    """
    Input: -
    Output: state (matriz 4x4) con todos sus valores a 00

    Esta funcion se encarga de resetear el estado del cifrado AES
    """
    for i in range(0, 16):
        state[i % 4][i // 4] = '00'

def state2string():
    """
    Input: -
    Output: m (string) con el contenido del state

    Esta funcion se encarga de coger el contenido del state y pasarlo
    a un string
    """
    m = ''
    for i in range(0, 16):
        m += state[i % 4][i // 4]
    return(m)

# esta funcion se utiliza para juntar de 4 en 4 palabras como
# unicas entradas de un array, es decir, si antes tenias 8 palabras, 
# ahora tienes dos posiciones de array, con 4 palabras cada una.
def agrupar(L, k):
    """
    Input: L (lista) y k (int)
    Output: G (lista) con k palabras de L en cada posicion
    
    Esta funcion se utiliza para juntar de 4 en 4 palabras como
    unicas entradas de un array, es decir, si antes tenias 8 palabras, 
    ahora tienes dos posiciones de array, con 4 palabras cada una.
    """
    from functools import reduce
    assert len(L) % k == 0
    N = len(L) // k
    G = [L[k*i:k*i+k] for i in range(N)]
    return(reduce(lambda x, y: x + y, w) for w in G)




# ------ FUNCIONES DE CIFRADO ------

def sbox(b):
    """
    Input: b (bitarray)
    Output: val (bitarray) con el valor de la sustitucion de b

    Esta funcion se encarga de coger un bitarray de 8 bits y le aplica
    tabla de sustitucion según las coordenadas que dicten su valor
    numerico
    """
    x = b[:4]
    y = b[4:]
    x = ba2int(x)
    y = ba2int(y)

    val = SboxTable[x][y]
    val = hex2ba(val)
    return (val)

def Sbox(word):
    """
    Input: word (bitarray)
    Output: B (bitarray) con el valor de la sustitucion de word

    Sbox coge la palabra de 32 digitos binarios que le proporciona el 
    el return de SubWord y le aplica sbox a cada trozo de 8 bits 
    de la palabra, devolviendo un bitarray de 32 bits
    """
    B = bitarray() 
    for i in range(0,len(word),8):
        b = word[i:i+8]
        b = sbox(b)
        B = B + b
    return (B)

def RotWord(word): 
    """
    Input: word (bitarray)
    Output: word (bitarray) con el primer byte al final de la palabra

    RotWord coge el primer byte y le pone al final de la palabra.
    La variable word entra en formato binario y retorna otro bitarray
    """
    return(word[8:]+word[:8])

def SubWord(word):
    """
    Input: word (bitarray)
    Output: Sbox(word) (bitarray) con la sustitucion de cada byte
    de word

    SubWord coge los bytes que le entren en la variable word
    (en binario) y les aplica la sustitución de la funcion Sbox.
    """
    return Sbox(word) 

def KeyExpansion(key): 
    """
    Input: key (string)
    Output: w (lista) con el KeySchedule

    Nb = 4 Nk = 8 Nr = 14       Nb * (Nr + 1) = 60
    KeyExpansion es la funcion que genera el KeySchedule a partir de la
    clave que se le pasa como parametro. La clave entra en hexadecimal y
    se devuelve una lista de 15 palabras (bitarrays) de 128 bits cada 
    una
    """
    key = hex2ba(key) # key es un bitarray de 256 bits
    w = []

    # dividimos en palabras de 32 bits
    w = [key[32*i:32*i+32] for i in range(8)]

    i = 8 #Nk

    # aqui w es una lista de 8 palabras de 32 bits cada una
    # en cada iteracion se añade una nueva palabra al final de la lista w
    while i<60:
        temp = w[i-1]
        if i % 8 == 0:
            temp = SubWord(RotWord(temp))
            temp ^= Rcon[i//8 - 1]

        elif i%8 == 4:
            temp = SubWord(temp)

        temp = w[i-8]^temp

        w.append(temp)

        i += 1

    return(agrupar(w,4))

def AddRoundKey(key, round):    
    """
    Input: key (string) y round (int)
    Output: state (matriz 4x4) con el resultado de aplicar el XOR
    
    En AddRoundKey intercambiamos los valores del estado haciendo un XOR 
    del propio estado con 4 palabras del key schedule que nos devuelve
    la funcion keyExpansion. El state ya tiene que estar establecido
    con el contenido del mensaje
    """

    # keySchedule es una lista de 15 palabras de 128 bits cada una
    keySchedule = list(KeyExpansion(key))

    # keyScheduleYaPartido es una lista de 15 listas de 4 palabras de 32 bits
    # cada una, es decir, así podemos aplicar el XOR de cada lista de la
    # keyScheduleYaPartida con cada fila del state, que ambas tienen
    # 4 elementos
    keyScheduleYaPartido = []
    for palabra in keySchedule:
        keySchedulePartes = [['','','',''],['','','',''],['','','',''],['','','','']]
        palabraAux = ba2hex(palabra)
        for i in range(0, 16):
            aux2 = palabraAux[2*i:2*i+2]
            keySchedulePartes[i % 4][i // 4] = aux2
            # así, para cada iteracion del for, se llena cada casilla de la
            # matrix 4x4 de manera vertical como se puede ver en el paper del
            # cifrado AES
        keyScheduleYaPartido.append(keySchedulePartes)
    
    # aplicamos el XOR
    for i in range(0, 16):
            state[i % 4][i // 4] = ba2hex(hex2ba(state[i % 4][i // 4]) ^
                hex2ba(keyScheduleYaPartido[round][i % 4][i // 4]))

def subBytes():
    """
    Input: -
    Output: state (matriz 4x4) con el resultado de aplicar la sustitucion
    
    subBytes coge cada byte del state y le aplica la sustitucion de la
    funcion sbox
    """
    for i in range(0, 16):
            state[i % 4][i // 4] = ba2hex(sbox(hex2ba(state[i % 4][i // 4])))

def shiftRows():
    """
    Input: -
    Output: state (matriz 4x4) con el resultado de aplicar la rotacion
    
    shiftRows coge cada fila del state y la rota a la izquierda tantas
    veces como su indice
    """
    for i in range(0, 4):
        state[i] = state[i][i:] + state[i][:i]

def traspuesta(matrix):
    """
    Input: matrix (matriz 4x4)
    Output: E (matriz 4x4) con la matriz traspuesta

    traspuesta traspone la matriz que se le pase por parámetro y la
    devuelve. Se usa para poder aplicar la funcion mixColumns como si
    se tratase de filas en vez de columnas.
    """
    E = []
    for i in range(0, 4):
        E.append([matrix[j][i] for j in range(0, 4)])
    return(E)

def xtime(B):
    """
    Input: B (bitarray)
    Output: b (bitarray) con el resultado de aplicar la multiplicacion
    
    xtime es la funcion que se encarga de aplicar la multiplicacion por
    x a un binario que se le pase por parametro. En caso de ser mayor
    que 8 bits, se le aplica el polinomio de reduccion de Rijndael
    """
    b = B.copy()
    b.append(0) 
    if b[0]==0:
        del(b[0])
    else:
        b^=bitarray('100011011') # polinomio de reduccion de Rijndael
        del(b[0])
    return(b)

def multRijndael(fila):
    """
    Input: fila (lista)
    Output: aux (lista) con el resultado de aplicar la multiplicacion
    
    multRijndael es la funcion que se encarga de aplicar la multiplicacion
    de Rijndael a cada columna (realmente fila ya que se encuentra
    traspuesto) del state
    """
    aux = []
    for i in range(4):
        x = ba2hex(xtime(hex2ba(fila[0])) ^ xtime(hex2ba(fila[1])) ^ 
                   hex2ba(fila[1]) ^ hex2ba(fila[2]) ^ hex2ba(fila[3]))
        aux.append(x)
        fila.append(fila[0])
        del(fila[0])
    return (aux)

# mixColumns coge cada columna (coge cada fila de la matriz traspuesta) del state
# y le aplica la multiplicacion de Rijndael
def mixColumns():
    """
    Input: -
    Output: state (matriz 4x4) con el resultado de aplicar la
            multiplicacion
    
    mixColumns coge cada columna (coge cada fila de la matriz
    traspuesta) del state y le aplica la multiplicacion de Rijndael
    """
    global state
    state = traspuesta(state)   
    for i in range(4):
        state[i] = multRijndael(state[i])
    
    state = traspuesta(state)
    return(state)




# ------ FUNCIONES DE DESCIFRADO ------

def invShiftRows():
    """
    Input: -
    Output: state (matriz 4x4) con el resultado de aplicar la rotacion
    
    invShiftRows coge cada fila del state y la rota a la derecha tantas
    veces como su indice
    """
    for i in range(0, 4):
        state[i] = state[i][-i:] + state[i][:-i]

def invsbox(b):
    """
    Input: b (bitarray)
    Output: val (bitarray) con el valor de la sustitucion inversa de b
    
    invsbox coge un bitarray de 8 bits y le aplica tabla de sustitucion
    inversa
    """
    x = b[:4]
    y = b[4:]
    x = ba2int(x)
    y = ba2int(y)

    val = invSboxTable[x][y]
    val = hex2ba(val)
    return (val)

def invSubBytes():
    """
    Input: -
    Output: state (matriz 4x4) con el resultado de aplicar la
            sustitucion inversa
    
    invSubBytes coge cada byte del state y le aplica la sustitucion
    inversa de la funcion invsbox
    """
    for i in range(0, 16):
            state[i % 4][i // 4] = ba2hex(invsbox(hex2ba(state[i % 4][i // 4])))

def tresXtime(b):
    """
    Input: b (bitarray)
    Output: xtime(xtime(xtime(b))) (bitarray) con el resultado de
            aplicar la multiplicacion
            
    tresXtime es una funcion que comprime realizar 3 veces la funcion
    xtime a un binario
    """
    return(xtime(xtime(xtime(b))))

def mult09(b):
    """
    Input: b (bitarray)
    Output: tresXtime(b)^b (bitarray) con el resultado de aplicar la
            multiplicacion
    
    mult09 es la funcion que se encarga de aplicar la multiplicacion
    inversa de Rijndael a cada columna (realmente fila ya que se
    encuentra traspuesto) del state
    """
    return(tresXtime(b)^b)

def mult0b(b):
    """
    Input: b (bitarray)
    Output: tresXtime(b)^xtime(b)^b (bitarray) con el resultado de
            aplicar la multiplicacion
    
    mult0b es la funcion que se encarga de aplicar la multiplicacion
    inversa de Rijndael a cada columna (realmente fila ya que se
    encuentra traspuesto) del state
    """
    return(tresXtime(b)^xtime(b)^b)


def mult0d(b):
    """
    Input: b (bitarray)
    Output: tresXtime(b)^xtime(xtime(b))^b (bitarray) con el resultado
            de aplicar la multiplicacion
    
    mult0d es la funcion que se encarga de aplicar la multiplicacion
    inversa de Rijndael a cada columna (realmente fila ya que se
    encuentra traspuesto) del state
    """
    return(tresXtime(b)^xtime(xtime(b))^b)

def mult0e(b):
    """
    Input: b (bitarray)
    Output: tresXtime(b)^xtime(xtime(b))^xtime(b) (bitarray) con el
            resultado de aplicar la multiplicacion
    
    mult0e es la funcion que se encarga de aplicar la multiplicacion
    inversa de Rijndael a cada columna (realmente fila ya que se
    encuentra traspuesto) del state
    """
    return(tresXtime(b)^xtime(xtime(b))^xtime(b))

def invMultRijndael(fila): 
    """
    Input: fila (lista)
    Output: aux (lista) con el resultado de aplicar la multiplicacion

    invMultRijndael es la funcion que se encarga de aplicar la
    multiplicacion inversa de Rijndael a cada columna (realmente fila
    ya que se encuentra traspuesto) del state
    """
    aux = []
    for i in range(4):
        x = ba2hex(mult0e(hex2ba(fila[0])) ^ mult0b(hex2ba(fila[1])) ^ 
                   mult0d(hex2ba(fila[2])) ^ mult09(hex2ba(fila[3])))
        aux.append(x)
        fila.append(fila[0])
        del(fila[0])
    return (aux)

def invMixColumns():
    """
    Input: -
    Output: state (matriz 4x4) con el resultado de aplicar la
            multiplicacion inversa 
    
    invMixColumns coge cada columna (coge cada fila de la matriz
    traspuesta) del state y le aplica la multiplicacion inversa de
    Rijndael
    """
    global state
    state = traspuesta(state)   
    for i in range(4):
        state[i] = invMultRijndael(state[i])
    
    state = traspuesta(state)
    return(state)



# ------ CIFRADO Y DESCIFRADO AES ------

def cifrado(key, mensaje):
    """
    Input: key (string) y mensaje (string)
    Output: state (matriz 4x4) con el mensaje cifrado
    
    cifrado recibe la clave y el mensaje en hexadecimal y modifica
    durante su ejecución el state para que al finalizar el mensaje
    cifrado se encuentre en esa matriz
    """
    global state

    setState(mensaje)

    AddRoundKey(key, 0)

    for i in range(1, 14):
        subBytes()
        shiftRows()
        mixColumns()
        AddRoundKey(key, i)
    
    subBytes()
    shiftRows()
    AddRoundKey(key, 14)

def descifrado(key, mensaje):
    """
    Input: key (string) y mensaje (string)
    Output: state (matriz 4x4) con el mensaje descifrado

    descifrado recibe la clave y el mensaje en hexadecimal y modifica
    durante su ejecución el state para que al finalizar el mensaje
    descifrado se encuentre en esa matriz
    """

    global state

    setState(mensaje)

    AddRoundKey(key, 14)

    for i in reversed(range(1, 14)):
        invShiftRows()
        invSubBytes()
        AddRoundKey(key, i)
        invMixColumns()
    
    invShiftRows()
    invSubBytes()
    AddRoundKey(key, 0)




# ------ GESTIÓN DE MENSAJES CIFRADOS Y PARA CIFRAR ------

def padding(mensaje):
    """
    Input: mensaje (string)
    Output: m (string) con el mensaje con el padding añadido
    
    padding es la funcion que se encarga de añadir los bits necesarios
    a un trozo del mensaje para que sea multiplo de 32 bits
    """
    m = mensaje + '80'
    L = len(m)
    r = L % 32
    if r != 0:
        m += '0' * (32-r)
    return(m)

def hex2str(h):
    """
    Input: h (string)
    Output: ''.join(Letras) (string) con el mensaje en ascii
    
    hex2str es la funcion que se encarga de traducir de hexadecimal a
    string
    """
    H = [h[i:i+2] for i in range(0, len(h), 2)]
    L = [int(x, 16) for x in H]
    Letras = [chr(n) for n in L]
    return(''.join(Letras))

def str2hex(cadena):
    """
    Input: cadena (string)
    Output: ''.join([hex(ord(letra))[2:] for letra in cadena]) (string)
            con el mensaje en hexadecimal
    
    str2hex es la funcion que se encarga de traducir de string a
    hexadecimal
    """
    return(''.join([hex(ord(letra))[2:] for letra in cadena]))

def msg2blockArray(mensaje):
    """
    Input: mensaje (string)
    Output: m (lista) con el mensaje dividido en bloques de 128 bits

    msg2blockArray es la funcion que se encarga de dividir el mensaje
    en bloques de 128 bits para poder cifrarlo por trozos en el caso
    de ser un mensaje mayor que 128 bits
    """
    m = []
    for i in range(0, len(mensaje), 32):
        m.append(mensaje[i:i+32])
    return(m)



# ------ MENÚ PRINCIPAL ------

def tituloPrograma():
    print('\n~~~~~~~~~~~~~~~~')
    print('    MENÚ AES')
    print('~~~~~~~~~~~~~~~~')

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
     
    print ("\nSaliendo... Hasta pronto! :)\n")
    
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
        print('Error, la clave debe tener 64 caracteres')
        key = input("Introduzca la clave en formato hexadecimal: ")    
    
    while(not valido):
        try:
            mensaje = input('Escriba el mensaje en texto plano que desea \
cifrar: ')
            mensaje = str2hex(mensaje)
            longitud= len(hex2ba(mensaje))
            if(longitud<128):
                mensaje = padding(mensaje)
            valido=True
        except ValueError:
            print('Error, no introduzca simbolos ni caracteres especiales')
               
    if(len(hex2ba(mensaje))==128):
        cifrado(key,mensaje)
        mensajeC = state2string()
        print('\nEl mensaje cifrado en Hex es: ', mensajeC+'\n')
        resetState()

    if(len(hex2ba(mensaje))>128):
        messageArray = msg2blockArray(mensaje)
        if(len(hex2ba(messageArray[-1]))<128):
            messageArray[-1] = padding(messageArray[-1])
        for block in messageArray:
            cifrado(key, block)
            mensajeC += state2string()
            resetState()
        print('\nEl mensaje cifrado en Hex es: ', mensajeC+'\n')

    tituloPrograma()

def opt2():
    
    mensajeD=''
    mensaje=''
    key=''
    valido=False
    
    key = input("Introduzca la clave en formato hexadecimal: ")
    
    while(len(key)!=64):
        print('Error, la clave debe tener 64 caracteres')
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
        resetState()
        print('\nEl mensaje descifrado es: ')
        print('\nHex: ', mensajeD)
        print('Ascii: ', hex2str(mensajeD) + '\n')

    if(len(hex2ba(mensaje))>128):
        messageArray = msg2blockArray(mensaje)
        for block in messageArray:
            descifrado(key, block)
            mensajeD += state2string()
            resetState()
        print('\nEl mensaje descifrado es: ')
        print('\nHex: ', mensajeD)
        print('Ascii: ', hex2str(mensajeD) + '\n')

    tituloPrograma()

def main():
    
    tituloPrograma()

    menu_principal()

if __name__ == '__main__':
    main()