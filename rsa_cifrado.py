import random
def mcd(a, b):
    """SE IMPLEMENTA AGORITMO DE EUCLIDES PARA ENCONTRAR MCM"""
    while b!=0:
        a, b= b, a%b
        # Al numero mayor se lo divide entre el menor y se obtiene el cociente y el residuo, 
        # le tomamos en cuenta al residuo o modulo (%), hasta que este sea 0
    return a

def inverso_mod (e, phi):
    # Para el algoritmo extendido de euclides necesitamos a una clave e 
    # y un numero phi para crear una clave privada se necesita de un numero d
    # Segun RSA la clave e al ser multiplicada por d y divida para phi el residuo obligatoriamente es 1
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y
    if temp_phi == 1:
        return d + phi

def es_primo(num):
    """Comprueba si un número es primo"""
    if num < 2: 
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0: 
            return False
    return True

def generar_primo(rango_min=100, rango_max=999):
    """Genera un número primo aleatorio para p y q"""
    primo = random.randint(rango_min, rango_max)
    while not es_primo(primo):
        primo = random.randint(rango_min, rango_max)
    return primo

# --- 2. GENERACIÓN DE LLAVES RSA ---
def generar_llaves():
    # Paso 1: p y q
    p = generar_primo()
    q = generar_primo()
    while p == q: # Asegurarnos de que no sean el mismo número
        q = generar_primo()
        
    # Paso 2 y 3: Módulo (n) y Totiente (phi)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Paso 4: Llave Pública (e)
    e = random.randrange(1, phi)
    while mcd(e, phi) != 1:
        e = random.randrange(1, phi)
        
    # Paso 5: Llave Privada (d)
    d = inverso_mod(e, phi)
    return (e, n), (d, n)

# --- 3. CIFRADO Y DESCIFRADO ---
def cifrar(mensaje_plano, llave_publica):
    e, n = llave_publica
    # Convertimos cada letra a su código ASCII (ord), aplicamos la fórmula, 
    # y los unimos con comas para que viajen como un solo string.
    # pow(base, exponente, modulo) hace la fórmula (M^e) mod n eficientemente.
    cifrado = [str(pow(ord(letra), e, n)) for letra in mensaje_plano]
    return ",".join(cifrado)

def descifrar(mensaje_cifrado, llave_privada):
    d, n = llave_privada
    # Separamos por comas, aplicamos la fórmula inversa, y volvemos a letra (chr)
    partes = mensaje_cifrado.split(",")
    descifrado = [chr(pow(int(parte), d, n)) for parte in partes]
    return "".join(descifrado)