import socket
import json
import rsa_cifrado 

def iniciar_servidor():
    # Socket
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = '127.0.0.1' #por defecto
    puerto = 9999 #escogido al azar

    servidor.bind((host, puerto)) #Vincula el socket a una dirección y puerto
    servidor.listen(1) #En modo de espera, el 1 para aceptar solo a una persona.
    
    print(f"Servidor iniciado. Escuchando en {host}:{puerto}...")
    print("Esperando a que el cliente se conecte...")
    
    # Despues de la espera, devuelve nuevo socket y nueva direccion
    cliente_socket, direccion = servidor.accept()
    print(f"¡Conectado con: {direccion}!")
    
    try:
        # llaves de servidor
        mi_llave_pub, mi_llave_priv = rsa_cifrado.generar_llaves()
        mi_llave_pub, mi_llave_priv = rsa_cifrado.generar_llaves()
        print(f"Mi llave pública (servidor): {mi_llave_pub}")
        print(f"Mi llave privada (servidor): {mi_llave_priv}")

        # Recibir la llave publica del cliente y desempaquetar
        llave_cliente_cruda = cliente_socket.recv(4096).decode('utf-8')
        llave_pub_cliente = json.loads(llave_cliente_cruda)
        
        # Enviar llave publica al cliente empaquetada en json
        cliente_socket.send(json.dumps(mi_llave_pub).encode('utf-8'))
        print(" Intercambio de llaves exitoso ")
        print(" INICIO DEL CHAT \n")
        
        while True:
            # Se usa la nueva direccion, recibe datos cifrados
            # recv: determina hasta cuantos bytes se van a leer a la vez, decode: traduce a texto normal 
            mensaje_crudo = cliente_socket.recv(4096).decode('utf-8')

            print(f"[TRAMA CIFRADA RECIBIDA]: {mensaje_crudo}")
            # Si se corta la conexion abruptamente
            if not mensaje_crudo:
                print("\n El cliente ha abandonado el chat.")
                break
                
            # Descifrar mensaje del cliente usando llave privada
            mensaje_descifrado = rsa_cifrado.descifrar(mensaje_crudo, mi_llave_priv)
            
            # Si el cliente escribe 'salir', terminamos el chat
            if mensaje_descifrado.lower() == 'salir':
                print("\n El cliente ha abandonado el chat.")
                break
                
            print(f"[Cliente]: {mensaje_descifrado}")
            
            # El servidor escribe su respuesta
            respuesta = input("[Servidor]: ")
            
            # Si el servidor escribe 'salir', también cortamos
            if respuesta.lower() == 'salir':
                # Avisar al cliente que se interrumpe la comunicacion, mas se encripta
                despedida = rsa_cifrado.cifrar("salir", llave_pub_cliente)
                cliente_socket.send(despedida.encode('utf-8'))
                print("  Cerrando el chat...")
                break
            
            # Cifrar respuesta usando llave publica del cliente
            respuesta_cifrada = rsa_cifrado.cifrar(respuesta, llave_pub_cliente)
            
            # Con lo encriptado, se traduce a bytes y se envia al cliente
            cliente_socket.send(respuesta_cifrada.encode('utf-8'))
            
    except Exception as e:
        print(f"\n Ocurrió un error: {e}")
        
    finally:
        # Terminar comunicacion entre cliente y servidor 
        cliente_socket.close()
        servidor.close()
        print(" Conexiones cerradas correctamente.")

# si se ejecuta el archivo directamente, la funcion arranca
if __name__ == "__main__":
    iniciar_servidor()