import os
import socket
from time import *

#var
MAP = [[0,0,0],
       [0,0,0],
       [0,0,0]]
x = 0
y = 0
HEADER_SIZE = 1
FORMAT = "utf-8"

class bcolors:
    RED = '\033[1;31;47m'
    BLUE = '\033[1;34;47m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

#Function

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

def clear_map():
    global MAP
    MAP = [[0,0,0],
           [0,0,0],
           [0,0,0]]
    return

def print_map():
    print(" | 1 2 3")
    print("-+------")
    for i in range(0,3):
        print(f"{i+1}|",end="")
        for p in MAP[i]:
            if p == 0:
                print("  ",end="")
            elif p == 1:
                print("* ",end="")
            elif p == 2:
                print("0 ",end="")
        print()
    return

def check_grid(team=1):
    isWin = False

    if MAP[0][0]==team and MAP[1][1]==team and MAP[2][2]==team:
        isWin = True
    elif MAP[0][2]==team and MAP[1][1]==team and MAP[2][0]==team:
        isWin = True

    if not isWin:
        for i in range(0,3):
            if MAP[i][0]==team and MAP[i][1]==team and MAP[i][2]==team:
                isWin = True
                break

    if not isWin:
        for i in range(0,3):
            if MAP[0][i]==team and MAP[1][i]==team and MAP[2][i]==team:
                isWin = True
                break

    return isWin

def askForMov(team=1):
    clear()
    print(f"Choisissez votre case joueur {team}")
    print_map()

    isCorrect = False

    while not isCorrect:
        try:
            x = int(input("Colonne : "))-1
            y = int(input("Ligne : "))-1

            if MAP[y][x] != 0:
                print("Choix invalide")
            else:
                isCorrect = True
        except:
            print("Nombre invalide")

    MAP[y][x] = team
    return [x,y]

def soloGame():
    numOfTurn = 0
    whoWin = 0
    while whoWin==0:
        numOfTurn+=2
        askForMov(1)
        isWin = check_grid(1)
        if isWin:
            whoWin=1
            print("Joueur 1 a gagné")
            break
        if numOfTurn>=9:
            print("Match nul")
            break
        askForMov(2)
        isWin = check_grid(2)
        if isWin:
            whoWin=1
            print("Joueur 2 a gagné")
            break
    sleep(3)
    clear_map()
    return

def MultGameClient():
    PORT = int(input("Sur quel port : "))
    IP = input("Sur quel ip : ")
    ADDR = (IP,PORT)

    clear()
    print(f"Envoie d'une requête à {IP} au port {PORT}")
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(ADDR)
    except:
        print("Serveur déconnecter")

    print("Connection réussite")
    server_msg = client.recv(HEADER_SIZE).decode(FORMAT)
    if server_msg=="O":
        print("Serveur valide, lancement du code de validation")
        client.send(("M").encode(FORMAT))
    else:
        print("Serveur invalide, abordage")
        return

    clear()
    numOfTurn = 0
    whoWin = 0
    print_map()
    while not whoWin:
        numOfTurn+=2
        try:
            x = int(client.recv(HEADER_SIZE).decode(FORMAT))
            y = int(client.recv(HEADER_SIZE).decode(FORMAT))
        except:
            print("Il semble que le joueur c'est déconnecté. Fin de parti.")
            break
        MAP[y][x] = 1
        clear()
        print_map()
        isWin = check_grid(1)
        if isWin:
            whoWin=1
            print("Joueur 1 a gagné")
            break
        if numOfTurn>=9:
            print("Match nul")
            break

        r = askForMov(2)
        client.send((str(r[0])+str(r[1])).encode(FORMAT))
        clear()
        print_map()
        isWin = check_grid(2)
        if isWin:
            whoWin=1
            print("Joueur 2 a gagné")
            break
    sleep(3)
    clear_map()
    return
    

def MultGameServer():
    PORT = int(input("Sur quel port : "))
    IP = "0.0.0.0"
    ADDR = (IP,PORT)

    clear()
    print(f"Initialisation du serveur sur le port {PORT}")
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
    except:
        print("Port invalide")
        return

    isCorrect = False
    while not isCorrect:
        print("Attente de joueur...")
        client,addr_c = server.accept()
        print(f"[nouvelle connection] {addr_c}")
        print("Vérification du client...")
        client.send(("O").encode(FORMAT))
        client_msg = client.recv(HEADER_SIZE).decode(FORMAT)
        if client_msg=="M":
            print("Connection valide")
            isCorrect = True
        else:
            print("Connection invalide")

    clear()
    numOfTurn = 0
    whoWin = 0
    while not whoWin:
        numOfTurn+=2
        r = askForMov(1)
        client.send((str(r[0])+str(r[1])).encode(FORMAT))
        clear()
        print_map()
        isWin = check_grid(1)
        if isWin:
            whoWin=1
            print("Joueur 1 a gagné")
            break
        if numOfTurn>=9:
            print("Match nul")
            break

        try:
            x = int(client.recv(HEADER_SIZE).decode(FORMAT))
            y = int(client.recv(HEADER_SIZE).decode(FORMAT))
        except:
            print("Il semble que le joueur c'est déconnecté. Fin de parti.")
            break
        MAP[y][x] = 2
        clear()
        print_map()
        isWin = check_grid(2)
        if isWin:
            whoWin=1
            print("Joueur 2 a gagné")
            break
    sleep(3)
    clear_map()
    return

def init():
    while True:
        print(f"{bcolors.BOLD}MORPION{bcolors.ENDC}")
        print()
        print("1 - Jouer solo")
        print("2 - Lancer une parti en ligne")
        print("3 - Rejoindre une parti en ligne")
        print("4 - Quitter")

        try:
            r = int(input("Quoi faire : "))
        except:
            print("Il faut que ce soit un nombre")
            sleep(2)

        clear()

        if r==1:
            clear_map()
            soloGame()
        elif r==2:
            clear_map()
            MultGameServer()
        elif r==3:
            clear_map()
            MultGameClient()
        elif r==4:
            return

init()
