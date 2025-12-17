import socket
import threading

#indirizzo IP  e PORTA su cui voglia che il server sia in ascolto
IP = "0.0.0.0"#riceve da chiunque
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP,PORT))#mettiamo IP e PORT come parametri e cosi il server si mette in ascolto
    server.listen(5)#diciamo al server di mettersi in attesa di contatti, accettando fino a un massimo
                    #di 5 connessioni
    print(f"[*]Listening on {IP}:{PORT}")

    while True:#il programma rimane in un ciclo in cui attende le connessioni in entrata
        client, adress = server.accept()#quando un client si connette vengono immagazzinati il socket
                                        #client nella variabile client e i dettagli della connessione 
                                        #in adress!
        print(f"[*]Accepted connection from {adress[0]}:{adress[1]}")
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()#viene avviato il thread che inizia ad occuparsi del dialogo, e il server
                              #è così pronto a gestire una nuova chiamata in ingresso

def handle_client(client_socket):#il server invia un messaggio di risposta al client
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*]Recived: {request.decode("utf-8")}')
        sock.send(b"RISPOSTA")

if __name__ == "__main__":
    main()