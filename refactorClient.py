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
        #noErrorOccured = True
        # Send a request to the server
        request = input(Config.request1Message)
        socket.send(request.encode())
        response = socket.recv(1024).decode()
        # Check status
        if isinstance(response, str):
            if response == Config.invalidDayInput:
                print(Config.invalidDayInput)
                print(Config.tryAgain)
                #noErrorOccured = False
                continue
            # Input prea scurt / lung
            if response ==  Config.tooLongRequest:
                print(Config.tooLongRequest)
                print(Config.tryAgain)
                #noErrorOccured = False
                continue
            # Request scris gresit
            if response == Config.badRequestIndex0:
                print(Config.badRequestIndex0)
                print(Config.tryAgain)
               # noErrorOccured = False
                continue
            if response == Config.badRequestIndex1:
                print(Config.badRequestIndex1)
                print(Config.tryAgain)
                #noErrorOccured = False
                continue
            if response == Config.badRequestIndex2:
                print(Config.badRequestIndex2)
                print(Config.tryAgain)
                #noErrorOccured = False
                continue
            # O exceptie care nu e gestionata explicit
            if response == Config.unhandeledExceptionOccured:
                print(Config.unhandeledExceptionOccured)
                print(Config.tryAgain)
                #noErrorOccured = False
                continue

  # 2nd Request is send
        if response == Config.requestProcessed:
            request = input(Config.request2Message)
            socket.send(request.encode())
            request = request.split("/")

            response = socket.recv(1024).decode()
            if(isinstance(response, str)):
                print("Response ul este string, dar nu ar trebui")
                print(response)
                #noErrorOccured = False
                continue
        # daca avem un request specific, atunci o sa primim 2 informatii de la server: 1.Orele(array), 2.Detaliile (jsonDoc serializat)
            if len(request) > 1:
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
                deserializedResponse = json.loads(response)
                for hour in deserializedResponse:
                    print(hour)
                    for detailName in deserializedResponse[hour]:
                        print(detailName +": "+ deserializedResponse[hour][detailName])

        #if(noErrorOccured):
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
        # userInput = input("Do you need any more help ? Y/N\n")
        # if userInput != 'Y':
        #     stillRunning = False

# Close the connection
socket.close()



import socket
import json

# Create a socket object
from config import Config

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
socket.connect(("localhost", 12121))



while True:
    #1 Dialog 1 - START / STOP
    userWantsToStop = False
    while True:
        userSaysStart = input("1.START\n2.STOP\n")
        if userSaysStart.upper() == "STOP":
            socket.send("STOP".encode())
            userWantsToStop = True
            break
        if userSaysStart.upper() == "START":
            socket.send("START".encode())
            break
        if userSaysStart.upper() != "START":
            print("Invalid input.")
            continue
    if userWantsToStop == True:
        break


    #3 Dialog 2 - REQ 1
    errorOccured = False
    while True:
            # recv req1
        serverResponse = socket.recv(1024).decode()
        if serverResponse != Config.request1Message:
                print("ERROR. Server response = " + serverResponse)
                print("Response expected " + Config.request1Message)
                errorOccured = True
                break
        if errorOccured == True:
            print("Requests got stuck probably. Error occured first req!")
            break

        #3 Dialog 2 - REQ 1
            # manage inputi untill correct
        requestProcessedSent = False
        while True:
            request = input(Config.request1Message)
            socket.send(request.encode())
            serverResponse = socket.recv(1024).decode()

            # Input prea scurt / lung
            if serverResponse ==  Config.tooLongRequest:
                print(Config.tooLongRequest)
                print(Config.tryAgain)
                continue
            # Request scris gresit
            if serverResponse == Config.badRequestIndex0:
                print(Config.badRequestIndex0)
                print(Config.tryAgain)
                continue
            if serverResponse == Config.badRequestIndex1:
                print(Config.badRequestIndex1)
                print(Config.tryAgain)
                continue
            if serverResponse == Config.badRequestIndex2:
                print(Config.badRequestIndex2)
                print(Config.tryAgain)
                continue
            if serverResponse == Config.requestProcessed:
                requestProcessedSent = True
                break
        if requestProcessedSent:
            break
    if(errorOccured):
        break

    #3 Dialog 3 - REQ 2
    while True:
        serverResponse = socket.recv(1024).decode()
        if serverResponse != Config.request2Message:
            print("ERROR. Server response = " + serverResponse)
            print("Response expected " + Config.request2Message)
            errorOccured = True
            break
        if errorOccured:
            print("Requests got stuck probably. Error occured second req!")
            break

        requestProcessedSent = False
        requestHaveOptions = False
        while True:
            request = input(Config.request2Message)
            socket.send(request.encode())
            serverResponse = socket.recv(1024).decode()

            if serverResponse == Config.invalidOptionInput:
                print(Config.invalidOptionInput)
                print(Config.tryAgain)
                continue
            if serverResponse == Config.invalidDayInput:
                print(Config.invalidDayInput)
                print(Config.tryAgain)
                continue
            if serverResponse == Config.requestProcessed:
                requestProcessedSent = True
                if len(request.split("/")) > 1:
                    requestHaveOptions = True
                break
        if requestProcessedSent:
            break
    if errorOccured:
        break

    #receive and siplay server response
    if not requestHaveOptions:
        serverResponse = socket.recv(1024).decode()
        deserializedResponse = json.loads(response)
        for hour in deserializedResponse:
            print(hour)
            for detailName in deserializedResponse[hour]:
                print(detailName +": "+ deserializedResponse[hour][detailName])
    if requestHaveOptions:
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
