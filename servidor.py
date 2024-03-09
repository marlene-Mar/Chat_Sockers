import socket
import threading
import sys
import pickle

class Servidor():

    #Se define el host y el puerto
    def __init__(self, host="localhost", port=4000):

        #Arreglo de clientes
        self.clientes = []

         #Variable que almacena el socket, que serpa TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Se enlaza con el cliente
        self.sock.bind((str(host), int(port)))
        #Maximo de conexiones
        self.sock.listen(10)
        self.sock.setblocking(False)

        #Hilos para procesar y aceptar las conversaciones
        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)

        aceptar.daemon = True
        aceptar.start()

        procesar.daemon = True
        procesar.start()

        while True:
            msg= input('->')
            if msg == 'salir':
                self.sock.close()
                sys.exit()
            else:
                pass

    #Proceso para enviar el mismo mensaje a los clientes conectados
    def msg_to_all(self,msg,cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)
            except:
                #Si no permite enviarle mensaje al cliente, se remueve el cliente ya que no existe una conexion correcta
                self.clientes.remove(c)

    #Proceso para aceptar conexion
    def aceptarCon(self):
        print("aceptarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass
    
    #Proceso para procesar conexión
    def procesarCon(self):
        print("ProcesarCon Iniciado")
        while True:
            if len(self.clientes) > 0:
                #Se verifica que cada cliente del arreglo de clientes reciba un mensaje
                for c in self.clientes:
                    try:
                        data = c.recv(10124)
                        if data:
                            self.msg_to_all(data,c)
                    except:
                        pass
#Inicializando el servidor
s = Servidor()

         
