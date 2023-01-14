import socket
import json

# Create a socket object
from config import Config

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect(("localhost", 12121))


#1 Conditie necesara pentru comanda START
while(True):
    userSaysStart = input("1.START\n2.STOP\n")
    if userSaysStart.upper() == "STOP":
        break
    if userSaysStart.upper() != "START":
        continue

    s.send("START".encode())

#2 Serverul raspunde clientului ca asteapta socilitarea de tipul e.g.
    serverResponse = s.recv(1024).decode()
    if serverResponse != Config.request1Message:
        print("ERROR. Server response = " + serverResponse)
        continue

#3 Studentul intrudce requestul
    stillRunning = True
    while(stillRunning):
        # Send a request to the server
        request = input(Config.request1Message)
        s.send(request.encode())

        # Receive request status from the server
        response = s.recv(1024).decode()

        if isinstance(response, str):

            # Input prea scurt / lung
            if response ==  Config.tooShortLongRequest:
                print(Config.tooShortLongRequest)
                print(Config.tryAgain)
                continue
            # Request scris gresit
            if response == Config.badRequestIndex0:
                print(Config.badRequestIndex0)
                print(Config.tryAgain)
                continue
            if response == Config.badRequestIndex1:
                print(Config.badRequestIndex1)
                print(Config.tryAgain)
                continue
            if response == Config.badRequestIndex2:
                print(Config.badRequestIndex2)
                print(Config.tryAgain)
                continue
            # O exceptie care nu e gestionata explicit
            if response == Config.unhandeledExceptionOccured:
                print(Config.unhandeledExceptionOccured)
                print(Config.tryAgain)
                continue
            # 2nd Request is send
            if response == Config.requestProcessed:
                request = input(Config.request2Message)
                s.send(request.encode())

        # daca avem un request specific, atunci o sa primim 2 informatii de la server: arr de ore si detaliile despre orar
        if len(request.split("/")) > 1:
            response = s.recv(1024).decode()
            hours = response
            response = s.recv(1024).decode()
            deserializedResponse = json.loads(response)
            for hour in hours:
                print(hour)
                for valueName in deserializedResponse:
                    print("valName " + valueName +", val"+deserializedResponse[valueName])
        else:
            response = s.recv(1024).decode()
            deserializedResponse = json.loads(response)


        # Ask for next operation
        while(True):
            userInput = input("Do you need any more help ? Y/N\n")
            if userInput == 'Y':
                stillRunning = True
                break
            elif userInput == 'N':
                stillRunning = False
                break
            else:
                print("Bad input!")

# Close the connection
s.close()
