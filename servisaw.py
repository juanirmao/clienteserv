import socket  # Importa la biblioteca de sockets para la comunicación en red

# Configuración del servidor
direccion_del_Servidor = 'localhost'  # Defino la dirección del servidor como localhost (servidor local)
puerto_Servidor = 8080  # Establezco el puerto 8080 en el que el servidor escuchará las conexiones

# Creo un socket de servidor utilizando la familia de direcciones IPv4 (AF_INET) y el protocolo TCP (SOCK_STREAM)
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.bind((direccion_del_Servidor, puerto_Servidor))  # Asocio el socket a la dirección y puerto configurados
servidor_socket.listen(5)  # El servidor comenzará a escuchar hasta 5 conexiones en cola
print("Servidor esperando conexiones...")  # Imprime un mensaje en consola indicando que el servidor está activo y esperando conexiones

# Bucle principal que mantiene al servidor escuchando indefinidamente
while True:
    # Acepto una conexión entrante
    conexion, direccion = servidor_socket.accept()  # Acepto la conexión del cliente y almaceno la conexión y la dirección del cliente
    print(f"Conexión establecida con {direccion}")  # Muestra en consola la dirección IP y el puerto del cliente conectado
    
    # Bucle para la comunicación continua con el cliente conectado
    while True:
        # Recibo un mensaje de hasta 1024 bytes del cliente
        mensaje = conexion.recv(1024).decode('utf-8')  # Decodifico el mensaje recibido del cliente de formato UTF-8
        if not mensaje or mensaje.lower() == "salir":  # Si el mensaje está vacío o el cliente envía "salir"
            print(f"Conexión cerrada con {direccion}")  # Imprime un mensaje en consola indicando que se cierra la conexión con el cliente
            break  # Salgo del bucle de comunicación para cerrar la conexión

        print(f"Mensaje recibido: {mensaje}")  # Muestra en consola el mensaje recibido del cliente
        # Respondo al cliente con una confirmación de que el mensaje fue recibido
        conexion.send(f"Servidor: Recibido '{mensaje}'".encode('utf-8'))  # Envío la respuesta codificada en UTF-8 al cliente

    # Cierro la conexión con el cliente
    conexion.close()  # Cierro el socket para la conexión con este cliente específico
