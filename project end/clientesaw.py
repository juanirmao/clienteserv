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
