import socket
import json
import rsa_cifrado 

def iniciar_cliente():
    # Preparar el socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1' # por defecto
    puerto = 9999 # mismo que servidor.py
    
    try:
        # Se ejecuta en el try, si el servidor no esta la linea falla
        cliente.connect((host, puerto))
        print(f" Conectado al servidor en {host}:{puerto}")
        
        # Generar llaves de cliente
        mi_llave_pub, mi_llave_priv = rsa_cifrado.generar_llaves()
        mi_llave_pub, mi_llave_priv = rsa_cifrado.generar_llaves()
        print(f"Mi llave pública (cliente): {mi_llave_pub}")
        print(f"Mi llave privada (cliente): {mi_llave_priv}")
        
        # Enviar llave publica al servidor empaquetada en json
        cliente.send(json.dumps(mi_llave_pub).encode('utf-8'))
        
        # Recibir llave publica del servidor y desempaquetar
        llave_servidor_cruda = cliente.recv(4096).decode('utf-8')
        
        llave_pub_servidor = json.loads(llave_servidor_cruda)
        
        print(" Intercambio de llaves exitoso")
        print("    INICIO DEL CHAT (Escribe 'salir' para terminar)    ")
        
        while True:
            # El cliente escribe su mensaje
            mensaje = input("[Cliente]: ")
            # Si el cliente decide salir, romper bucle
            if mensaje.lower() == 'salir':
                # Avisar al servidor la interrupcion pero se encripta
                despedida = rsa_cifrado.cifrar("salir", llave_pub_servidor)
                cliente.send(despedida.encode('utf-8'))
                print(" Has abandonado el chat.")
                break
                
            # Cifrar el mensaje con la llave del servidor
            mensaje_cifrado = rsa_cifrado.cifrar(mensaje, llave_pub_servidor)
            
            # Mensaje encriptado enviado al servidor en forma de bytes
            cliente.send(mensaje_cifrado.encode('utf-8'))
            
            # Despues del envio el cliente espera a que servidor envie una respuesta y la traduce
            respuesta_cruda = cliente.recv(4096).decode('utf-8')
            
            print(f"[TRAMA CIFRADA RECIBIDA]: {respuesta_cruda}")
            # Si el servidor cortó la conexión 
            if not respuesta_cruda:
                print(" El servidor ha cerrado el chat.")
                break
                
            # Descifrar la respuesta usando llave privada
            respuesta_descifrada = rsa_cifrado.descifrar(respuesta_cruda, mi_llave_priv)
            
            # Si el servidor manda la palabra salir
            if respuesta_descifrada.lower() == 'salir':
                print(" El servidor ha cerrado el chat.")
                break
                
            print(f"[Servidor]: {respuesta_descifrada}")     
            
    except ConnectionRefusedError:
        print(" Error: No se pudo conectar. ¿El servidor está encendido?")
    except Exception as e:
        print(f" Ocurrió un error inesperado: {e}")
        
    finally:
        # Se cierra comunicacion
        cliente.close()
        print("Conexión cerrada correctamente.")

if __name__ == "__main__":
    iniciar_cliente()