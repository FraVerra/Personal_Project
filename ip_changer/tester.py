import subprocess
import sys
'''
def boh():
    try:
        ssid_name = subprocess.run(["sudo","iwgetid","-r"], capture_output=True, text=True, check=True) 
        command_result = ssid_name.stdout[0:-1]
        print(command_result)
        file_name = f"{command_result}.txt"
        dir_create = subprocess.run(["mkdir","-p","ssid-default-ip"], capture_output=True, text=True, check=True)
    if dir_create.returncode == 0:
        print("cartella creata/già esistente")
    else:
        print("errore nel creare la cartella")
    try:
        file_ssid = open(f"ssid-default-ip/{file_name}","a")
        print("il file esiste gia")

    except FileNotFoundError:
        print("il file non esiste, procedo alla sua creazione")
        file_ssid = open(f"ssid-default-ip/{file_name}","w")
    file_ssid.write(command_result)

    except subprocess.CalledProcessError:
        print("non sei connesso alla rete")
        sys.exit()
'''
def createDir_file(dir_name, file_name):
    create_dir = subprocess.run(["mkdir","-p",dir_name], capture_output=True, check=True, text=True)
    if create_dir.returncode == 0:
        print("[*] The directory 'ssid-default-ip' alredy exist/has been created")
    else:
        print("[-] Fatal errore while creating the directory")
        sis.exit()
    try:
        ssid_file = open(f"{dir_name}/{file_name}","a")
    except FileNotFoundError:
        ssid_file = open(f"{dir_name}/{file_name}","w")
    
    ssid_file.close()
    ssid_file = open(f"{dir_name}/{file_name}","a")
    ssid_file.write(file_name+"\n")

def main():
    createDir_file("prova","oppio")

if __name__ == "__main__":
    main()