import socket
import threading
import sys
import pickle

class Cliente():

    #Se define el host y el puerto
    def __init__(self, host="locahost", port=4000):

        #Variable que almacena el socket, que serpa TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Nos conectamos al servidor
        self.sock.connect((str(host), int(port)))

        #Hilo que recibe los mensajes 
        msg_rec= threading.Thread(target=self.msg_rec)
        msg_rec.daemon = True #ayuda a no dejar un proceso abierto
        msg_rec.start()

        #Hilo que mantiene el hilo principal activo y nos permite mandar el mensaje
        while True:
            msg=input('->')
            if msg != 'salir':
                self.send_msg(msg)
            else:
                self.sock.close()
                sys.exit()



    #Funcion que recibe los mensajes
    def msg_rec(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(pickle.loads(data))
            except:
                pass
        
    #Funcion para enviar un mensaje
    def send_msg(self,msg):
        self.sock.send(pickle.dumps(msg))


# Instaciamos al cliente
c = Cliente(host="localhost")

            
