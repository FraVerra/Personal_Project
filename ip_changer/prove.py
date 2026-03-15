def scrittura(file):
    file.write("provaprova")

def main():
    file = open("ip_histori.txt", "w")
    scrittura(file) 

if __name__ == "__main__":
    main()