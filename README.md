**proyecto Cliente de Chat Simulado en Python**

He desarrollado una aplicación en Python que simula un cliente de chat utilizando Tkinter. El objetivo fue crear una interfaz gráfica sencilla y atractiva que permite la interacción con un servidor.

**Estructura del Proyecto**

El proyecto está compuesto por dos archivos:

- clientesaw.py: Este archivo contiene todo el código relacionado con la interfaz gráfica del cliente de chat.

- servisaw.py: Este archivo contiene el código del servidor que maneja las conexiones y responde a los mensajes del cliente.

**Requisitos**

Para poder ejecutar la aplicación, necesitas lo siguiente:

- Python 3.11.9 o superior.

- Tkinter (esta biblioteca viene incluida con la instalación estándar de Python en Windows, por lo que no deberías necesitar instalar nada adicional).

**Instalación**

**1.**cree los archivos clientesaw.py y servisaw.py y los guarde en un carpeta general con el nombre de cliente serv.

**2.**me asegure de tener las versiones adecuadas de python en este caso la version 3.11.9.

**Uso**

**1.**Abre una terminal o el símbolo del sistema en la carpeta donde guardaste los archivos.

**2.**Primero,se ejecuta el servidor con el siguiente comando:

**python servisaw.py**

**3.**Luego, en otra terminal, ejecute el cliente con el siguiente comando:

**python clientesaw.py**

**4.**Se abrirá una ventana del cliente donde se podra escribir mensajes en el campo de entrada y, al presionar el botón "Enviar", se simulará una conversación real con el servidor.

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

**Código de clientesaw.py**


import socket  # Módulo para crear conexiones de red (sockets)
import tkinter as tk  # Módulo para la creación de interfaces gráficas
from tkinter import scrolledtext, messagebox  # Submódulos de tkinter para áreas de texto desplazables y mensajes emergentes

# Clase que representa la interfaz gráfica y lógica del cliente de chat
class SimulacionCliente:
    def __init__(self, root):
        # Inicialización de la ventana principal
        self.root = root
        self.root.title("Cliente de Chat - Clientesaw")  # Título de la ventana
        self.root.geometry("500x600")  # Tamaño de la ventana
        self.root.config(bg="#1F2833")  # Color de fondo de la ventana

        self.conectado = False  # Bandera para verificar si el cliente está conectado al servidor
        self.cliente_socket = None  # Inicialmente, el socket del cliente es 'None'
        self.create_widgets()  # Método que crea los elementos gráficos de la interfaz

    # Método para crear y organizar los widgets (elementos gráficos) en la ventana
    def create_widgets(self):
        # Etiqueta del título de la aplicación
        title_label = tk.Label(self.root, text="Simulación de Chat", bg="#1F2833", fg="white", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)  # Posiciona el título con un margen de 10 píxeles

        # Área de texto desplazable para mostrar el chat
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20, bg="#2C3E50", fg="white", font=("Arial", 12))
        self.chat_area.pack(pady=10)  # Posiciona el área de chat con un margen superior
        self.chat_area.config(state=tk.DISABLED)  # Se desactiva la edición del área de chat

        # Campo de entrada para escribir mensajes
        self.entry_message = tk.Entry(self.root, width=40, font=("Arial", 14), bg="#F7F9F9", fg="#2C3E50")
        self.entry_message.pack(pady=5, padx=10, side=tk.LEFT, expand=True)  # El campo de entrada se expande horizontalmente

        # Botón para enviar mensajes
        self.btn_send = tk.Button(self.root, text="Enviar", command=self.send_message, bg="#E74C3C", fg="white", font=("Arial", 12))
        self.btn_send.pack(pady=5, padx=10, side=tk.RIGHT)  # Botón a la derecha del campo de entrada

        # Botón para conectarse al servidor
        self.btn_connect = tk.Button(self.root, text="Conectar", command=self.conectar_al_servidor, bg="#3498DB", fg="white", font=("Arial", 12))
        self.btn_connect.pack(pady=5, padx=10, side=tk.BOTTOM)  # Botón en la parte inferior de la ventana

        # Botón para cerrar la aplicación
        self.btn_exit = tk.Button(self.root, text="Salir", command=self.salir_aplicacion, bg="#E74C3C", fg="white", font=("Arial", 12))
        self.btn_exit.pack(pady=5, padx=10, side=tk.BOTTOM)  # Botón en la parte inferior, junto al botón de conectar

    # Método para conectar el cliente al servidor
    def conectar_al_servidor(self):
        if not self.conectado:  # Solo conecta si no está ya conectado
            try:
                # Crear el socket para conectar al servidor
                self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.cliente_socket.connect(('localhost', 8080))  # Se conecta al servidor en el puerto 8080 en localhost
                self.conectado = True  # Actualiza el estado de la conexión
                self.mostrar_mensaje("Conectado al servidor.")  # Muestra un mensaje en el área de chat
            except Exception as e:
                # Si ocurre un error, muestra un mensaje emergente con la descripción del error
                messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor: {e}")

    # Método para enviar un mensaje al servidor
    def send_message(self):
        if not self.conectado:  # Si no está conectado, muestra advertencia
            messagebox.showwarning("Desconectado", "Conéctate al servidor primero.")
            return  # Sale de la función si no está conectado

        message = self.entry_message.get()  # Obtiene el mensaje del campo de entrada
        if message:  # Si el mensaje no está vacío
            self.cliente_socket.sendall(message.encode('utf-8'))  # Envía el mensaje al servidor codificado en UTF-8
            # Actualiza el área de chat con el mensaje enviado
            self.chat_area.config(state=tk.NORMAL)  # Habilita temporalmente el área de chat
            self.chat_area.insert(tk.END, f"Tú: {message}\n")  # Inserta el mensaje enviado en el área de chat
            self.chat_area.config(state=tk.DISABLED)  # Desactiva el área de chat nuevamente para que sea solo de lectura
            self.entry_message.delete(0, tk.END)  # Limpia el campo de entrada de texto

            # Recibe la respuesta del servidor
            respuesta = self.cliente_socket.recv(1024).decode('utf-8')  # Espera la respuesta del servidor (máximo 1024 bytes)
            # Muestra la respuesta en el área de chat
            self.chat_area.config(state=tk.NORMAL)  # Habilita temporalmente el área de chat
            self.chat_area.insert(tk.END, f"{respuesta}\n")  # Inserta la respuesta del servidor
            self.chat_area.config(state=tk.DISABLED)  # Desactiva el área de chat nuevamente
        else:
            # Si no hay mensaje en el campo de entrada, muestra una advertencia
            messagebox.showwarning("Advertencia", "Escribe algo antes de enviar el mensaje.")

    # Método para mostrar mensajes en el área de chat
    def mostrar_mensaje(self, mensaje):
        self.chat_area.config(state=tk.NORMAL)  # Habilita temporalmente el área de chat
        self.chat_area.insert(tk.END, f"{mensaje}\n")  # Inserta el mensaje en el área de chat
        self.chat_area.config(state=tk.DISABLED)  # Desactiva el área de chat para solo lectura

    # Método para cerrar la aplicación
    def salir_aplicacion(self):
        self.root.destroy()  # Cierra la ventana de la aplicación y finaliza el programa

# Inicialización de la ventana principal de Tkinter
root = tk.Tk()  # Crea la ventana principal
app = SimulacionCliente(root)  # Instancia la clase SimulacionCliente y pasa la ventana como argumento
root.mainloop()  # Inicia el bucle principal de eventos de Tkinter



________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


**Código de servisaw.py**


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


________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

**Explicación del Código**

- Importaciones: Importo los módulos necesarios de Tkinter y socket para construir la interfaz gráfica y manejar la comunicación.

- Clase SimulacionCliente: Defino una clase que se encarga de manejar la interfaz del cliente de chat y la conexión con el servidor.

- Método _init_: Configuro la ventana principal, asignando su título, tamaño y color de fondo. Luego


- Método create_widgets: Este método crea todos los elementos de la interfaz gráfica, incluyendo etiquetas, área de chat, campo de entrada y botones. La configuración incluye estilos de colores y fuentes para una mejor experiencia de usuario.

- Método conectar_al_servidor: Este método intenta establecer una conexión con el servidor. Si la conexión es exitosa, se actualiza el estado del cliente y se muestra un mensaje de confirmación. En caso de error, se presenta un mensaje de advertencia.

- Método send_message: Este método envía el mensaje ingresado por el usuario al servidor. Primero, verifica si el cliente está conectado. Si el campo de entrada está vacío, se muestra una advertencia. Una vez enviado el mensaje, se recibe la respuesta del servidor y se muestra en el área de chat.

- Método mostrar_mensaje: Este método permite agregar mensajes al área de chat, habilitando temporalmente la edición del área para insertar el mensaje y deshabilitándola nuevamente para evitar modificaciones.

- Servidor (servisaw.py): Este archivo define la lógica del servidor que espera conexiones de los clientes. Al recibir un mensaje, lo imprime en la consola y responde con una confirmación. Si el cliente envía un mensaje vacío o "salir", se cierra la conexión.

**Objetivo**

Desarrollé este proyecto con el objetivo de crear una experiencia de chat interactiva y atractiva utilizando Python y Tkinter. Mi idea fue permitir a los usuarios interactuar con un servidor real, enfocándome más en la parte del cliente para facilitar tanto el desarrollo como la prueba de la aplicación de forma eficiente.
