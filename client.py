import socket
import json

# Create a socket object
from config import Config

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
socket.connect(("localhost", 12121))


#1 Conditie necesara pentru comanda START
while(True):
    userSaysStart = input("1.START\n2.STOP\n")
    if userSaysStart.upper() == "STOP":
        socket.send("STOP".encode())
        break
    if userSaysStart.upper() != "START":
        continue
    socket.send("START".encode())

#2 Clientul primeste raspunsul serverului - 'Trimite req 1 '
    serverResponse = socket.recv(1024).decode()
    if serverResponse != Config.request1Message:
        print("ERROR. Server response = " + serverResponse)
        continue

#3 Studentul introduce requestul
    stillRunning = True
    while(stillRunning):
        # Send a request to the server
        request = input(Config.request1Message)
        socket.send(request.encode())
        response = socket.recv(1024).decode()
        # Check status
        if isinstance(response, str):
            if response == Config.invalidDayInput:
                print(Config.invalidDayInput)
                print(Config.tryAgain)
                continue
            # Input prea scurt / lung
            if response ==  Config.tooLongRequest:
                print(Config.tooLongRequest)
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
            socket.send(request.encode())
        # daca avem un request specific, atunci o sa primim 2 informatii de la server: 1.Orele(array), 2.Detaliile (jsonDoc serializat)
            if len(request.split("/")) > 1:
                response = socket.recv(1024).decode()
                print("hours")
                print(response)
                hours = json.loads(response)
                response = socket.recv(1024).decode()
                print("deserializedResponse")
                print(response)
                deserializedResponse = json.loads(response)
                for hour in hours:
                    print(hour)
                    for valueName in deserializedResponse:
                        print(valueName +": "+deserializedResponse[valueName])
            else:
                response = socket.recv(1024).decode()
                deserializedResponse = json.loads(response)
                for hour in deserializedResponse:
                    print(hour)
                    for detailName in deserializedResponse[hour]:
                        print(detailName +": "+ deserializedResponse[hour][detailName])


        # Ask for next operation
        while(True):
            userInput = input("Do you need any more help ? Y/N\n")
            if userInput == 'Y':
                stillRunning = True
                socket.send("Y".encode())
                break
            elif userInput == 'N':
                stillRunning = False
                socket.send("N".encode())
                break
            else:
                print("Bad input!")

# Close the connection
socket.close()
