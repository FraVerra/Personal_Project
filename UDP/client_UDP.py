import socket

target_host = "45.33.32.156"#è un localhost un indirizzo IP che punta allo stesso computer(il mio)
target_port = 9997

#creazione dell'oggetto socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#SOCK_DRAMG indica il protocollo UDP

#invio dei dati
client.sendto(b"AAABBBCCC", (target_host,target_port))#sarebbe il messaggio da inviare

#ricezione della risposta
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()

#UDP non essendo un protocollo connesso non dobbiamo usare connect() ma solo recvfrom()