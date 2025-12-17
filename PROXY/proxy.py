#autore: Verra Francesco 
#proxy.py, costruzione di un proxy TCP
#definizione teoria di proxy: https://en.wikipedia.org/wiki/Proxy_server

'''
Quattro funzioni principali che ci serve scrivere:
- visualizzare i messaggi scambiati tra macchine locali e remote (hexdump)
- ricevere dati da una connessione in entrata via socket provenienti da macchina locale o remota(receive_from)
- ridirezinare il traffico di rete tra macchine locali e remote(proxy_handler)
- impostare un socket in ascolto e passargli il nostro proxy_handler
'''
#importazini di librerie utili

import sys
import socket
import threading

#questa stringa contiene caratteri ASCII, stampabili se ne esiste una rappresentazione, sennò stampa: '.'
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

#la funzione serve per leggere i dati che passano in tempo reale
def hexdump(src, lenght = 16, show = True):#la funzione riceve come input dei dati in formato binario(oppure stringa)
                                           #e ne va a stampare la versione esadecimale su console
    if isinstance(src, bytes):#verifichiamo se il dato sia una stringa, decodificando dati binari se necessario
        src = src.decode()
    results = list()
    for i in range(0,len(src), lenght):
        word = str(src[i:i+lenght])#prendiamo una porzione di stringa e la mettiamo dentro 'word'
        printable = word.translate(HEX_FILTER)#uso la funzione built-in 'translate' per sostituire la rappresentazione
                                              #stringa di ogni carattere con la corrispondente 'grezza'
        hexa = ''.join([f'{i:04x} {hexa:<{hexwidth}} {printable}'])

    if show:
        for line in results:
            print(line)
    else:
        return results

#questa funzione è usata per permettere la ricezione dei dati
def receive_from(connection):
    buffer = b""#creiamo una stringa binaria buffer che accumula risposte dal socket
    connection.settimeout(5)#impostiamo come valore ti timeout 5 secondi(da modificare in caso di forte traffico)
    try:
        while True:
            data = connection.recv(4096)#ciclo per leggere i dati in risposta e accodarli al buffer finchè non è 
                                        #finito l'afflusso o è scattato il timeout
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer#infine restituiamo il buffer al chiamante che potrebbe essere una macchina locale o remota

#funzioni che potrebbero servire per modificare dei pacchetti ii risposta o in richiesta, nel caso sostituire
#i commenti all'interno delle funzioni
def request_handler(buffer):
    #modifica dei pacchetti
    return buffer
def response_handler(buffer):
    #modifica dei pacchetti
    return buffer

#tale funzione contiene il cuore del proxy
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SO_STREAM)
    remote_socket.connect((remote_host, remote_port))#per iniziare ci connettiamo a un host remoto

    if(receive_first):#ci assicuriamo di non dover inizializzare una connessione con il lato server e richiedere
                      #dati prima di entrare nel ciclo
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)#passiamo l'output alla funzione response_handler
    if len(remote_buffer):
        print("[<==]Sending %d bytes to localhost." %len(remote_buffer))
        client_socket.send(remote_buffer)#inviamo i dati ricevuti al client locale

    while True:
        local_buffer = receive_from(client_socket)
        if(len(local_buffer)):
            line = "[==>]Received %d bytes from localhost." %len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>]Sent to remote.")
        
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==]Received %d bytes from remote." %len(remote_buffer))
            hexdump(remote_buffer)
            
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break