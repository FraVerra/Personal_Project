#pagine 14-15

#sia chi invia i dati che li riceve può usare questo programma: -c,-e,-u implicano degli argomenti

#importiamo prima tutte le librerie necessarie
import argparse  # libreria per creare interfacce da riga di comando (CLI)
import socket    # libreria per la comunicazione di rete (TCP/UDP)
import shlex     # parsifica stringhe di comandi in modo sicuro (divide argomenti)
import subprocess  # permette di eseguire comandi di sistema e catturarne l'output
import sys       # accesso a variabili e funzioni che interagiscono con l'interprete Python
import textwrap  # formattazione del testo (usato per l'help del programma)
import threading # permette di gestire connessioni multiple contemporaneamente

# FUNZIONE: esegue un comando di sistema e restituisce l'output
def execute(cmd):
    """
    Riceve un comando come stringa, lo esegue nel sistema operativo
    e restituisce l'output del comando
    """
    cmd = cmd.strip()  # Rimuove spazi bianchi all'inizio e alla fine
    if not cmd:        # Se il comando è vuoto, non fa nulla
        return
    # subprocess.check_output: esegue il comando e cattura l'output
    # shlex.split: divide il comando in una lista di argomenti in modo sicuro
    # stderr=subprocess.STDOUT: cattura anche gli errori (stderr) nell'output
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    
    return output.decode()  # Converte i bytes in stringa e la restituisce


# CLASSE PRINCIPALE: gestisce tutte le funzionalità del netcat
class NetCat:
    """
    Classe che implementa un tool simile a netcat per comunicazione di rete
    Può funzionare sia come client (invia dati) che come server (ascolta connessioni)
    """
    
    def __init__(self, args, buffer=None):
        """
        Inizializza l'oggetto NetCat
        args: argomenti passati da riga di comando (target, porta, modalità)
        buffer: dati da inviare (se presente)
        """
        self.args = args      # Salva gli argomenti (target IP, porta, opzioni)
        self.buffer = buffer  # ERRORE CORRETTO: mancava uno spazio tra buffer e self
        # Crea un socket TCP/IP:
        # AF_INET: famiglia di indirizzi IPv4
        # SOCK_STREAM: tipo di socket TCP (connessione affidabile)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Opzione SO_REUSEADDR: permette di riutilizzare subito la porta
        # (utile se il programma viene chiuso e riavviato rapidamente)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        """
        Punto di ingresso principale: decide se ascoltare o inviare
        """
        if self.args.listen:  # Se l'opzione -l è attiva, diventa un server
            self.listen()
        else:                 # Altrimenti diventa un client e invia dati
            self.send()

    def send(self):
        """
        MODALITÀ CLIENT: si connette a un server remoto e invia/riceve dati
        """
        # Connessione al target (IP) e alla porta specificati
        self.socket.connect((self.args.target, self.args.port))
        
        # Se c'è un buffer (dati da stdin), lo invia subito
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            # Ciclo infinito per mantenere la connessione aperta
            while True:
                recv_len = 1      # Variabile per controllare se ci sono dati ricevuti
                response = ''     # Stringa per accumulare la risposta
                
                # Ciclo interno: riceve dati fino a quando non ci sono più
                while recv_len:
                    data = self.socket.recv(4096)  # Riceve fino a 4096 bytes alla volta
                    recv_len = len(data)           # Lunghezza dei dati ricevuti
                    response += data.decode()      # Converte bytes in stringa e accumula
                    
                    # Se ricevuti meno di 4096 bytes, significa che è finito il messaggio
                    if recv_len < 4096:
                        break
                
                # Se c'è una risposta, la stampa
                if response:
                    print(response)
                    # Chiede all'utente di inserire un nuovo comando/messaggio
                    buffer = input('> ')
                    buffer += '\n'  # Aggiunge newline per indicare fine del comando
                    # Invia il messaggio al server
                    self.socket.send(buffer.encode())

        except KeyboardInterrupt:  # Se l'utente preme CTRL+C
            print('User terminated.')
            self.socket.close()    # Chiude il socket
            sys.exit()             # Esce dal programma

    def listen(self):
        """
        MODALITÀ SERVER: ascolta connessioni in arrivo
        """
        # Associa il socket all'indirizzo IP e alla porta
        self.socket.bind((self.args.target, self.args.port))
        # Inizia ad ascoltare, con una coda massima di 5 connessioni
        self.socket.listen(5)
        
        print(f"[*] Listening on {self.args.target}:{self.args.port}")  # Feedback all'utente
        
        # Ciclo infinito per accettare connessioni multiple
        while True:
            # accept() blocca il programma fino a quando un client si connette
            # Restituisce: socket del client e indirizzo del client
            client_socket, client_address = self.socket.accept()  # ERRORE CORRETTO: era solo "_"
            
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
            
            # Crea un nuovo thread per gestire questo client
            # (così il server può gestire più client contemporaneamente)
            client_thread = threading.Thread(
                target=self.handle,        # ERRORE CORRETTO: era handle_client, ora è handle
                args=(client_socket,)      # Passa il socket del client come argomento
            )
            client_thread.start()  # Avvia il thread

    def handle(self, client_socket):  # ERRORE CORRETTO: era "selfa"
        """
        Gestisce un singolo client connesso
        Decide cosa fare in base alle opzioni da riga di comando
        """
        
        # OPZIONE -e: esegue un comando e restituisce l'output
        if self.args.execute:
            output = execute(self.args.execute)  # Esegue il comando
            client_socket.send(output.encode())  # Invia l'output al client
        
        # OPZIONE -u: riceve un file dal client e lo salva
        elif self.args.upload:
            file_buffer = b''  # ERRORE CORRETTO: era 'b' (stringa), ora è b'' (bytes vuoto)
            
            # Ciclo per ricevere tutti i dati del file
            while True:
                data = client_socket.recv(4096)  # Riceve blocchi di 4096 bytes
                if data:
                    file_buffer += data  # Accumula i dati
                else:
                    break  # Se non ci sono più dati, esce dal ciclo
            
            # Salva i dati ricevuti nel file specificato
            with open(self.args.upload, 'wb') as f:  # 'wb' = write binary
                f.write(file_buffer)
            
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())  # Conferma al client
        
        # OPZIONE -c: apre una shell interattiva
        elif self.args.command:
            cmd_buffer = b''  # Buffer per accumulare il comando
            
            while True:
                try:
                    # Invia il prompt al client
                    client_socket.send(b'BHP: #> ')
                    
                    # Riceve il comando fino a trovare un newline
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)  # Riceve 64 bytes alla volta
                    
                    # Esegue il comando ricevuto
                    response = execute(cmd_buffer.decode())
                    
                    # Se c'è output, lo invia al client
                    if response:
                        client_socket.send(response.encode())
                    
                    cmd_buffer = b''  # Resetta il buffer per il prossimo comando
                    
                except Exception as e:
                    print(f"server killed {e}")
                    self.socket.close()
                    sys.exit()


# PUNTO DI INGRESSO DEL PROGRAMMA
if __name__ == "__main__":
    """
    Questa sezione viene eseguita solo quando il file è lanciato direttamente
    (non quando viene importato come modulo)
    """
    
    # Crea il parser per gli argomenti da riga di comando
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',  # Descrizione del programma
        formatter_class=argparse.RawDescriptionHelpFormatter,  # Mantiene la formattazione dell'epilog
        # Esempi di utilizzo mostrati quando si usa --help
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c #comando shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt #caricamento file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" #esecuzione di un comando
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 #testo verso la porta del server 135
            netcat.py -t 192.168.1.108 -p 5555 #connessione al server
            '''))
    
    # Definizione degli argomenti accettati dal programma:
    
    # -c: apre una command shell interattiva
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    
    # -e: esegue un comando specifico
    parser.add_argument('-e', '--execute', help='execute specified command')
    
    # -l: modalità listener (server)
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    
    # -p: porta da usare (default: 5555)
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    
    # -t: indirizzo IP target (default: 192.168.1.203)
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')  # ERRORE CORRETTO: mancava
    
    # -u: nome del file da caricare
    parser.add_argument('-u', '--upload', help='upload file')
    
    # Parse degli argomenti passati da riga di comando
    args = parser.parse_args()
    
    # Decide da dove prendere i dati da inviare:
    if args.listen:
        # Se è in modalità listener, non invia nulla inizialmente
        buffer = ''
    else:
        # Se è in modalità client, legge dati da stdin (input standard)
        # Esempio: echo "test" | python netcat.py -t 192.168.1.203 -p 5555
        buffer = sys.stdin.read()

    # Crea l'oggetto NetCat con gli argomenti e il buffer
    nc = NetCat(args, buffer.encode())  # encode() converte la stringa in bytes
    
    # Avvia il programma
    nc.run()