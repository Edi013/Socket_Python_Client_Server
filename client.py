import socket
import json

# Create a socket object
from config import Config

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect(("localhost", 12121))

requestMessage = "Enter a request.\ne.g:ANI/Grupa1/Subgrupa1\n"
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
    if serverResponse != requestMessage:
        print("ERROR. Server response = " + serverResponse)
        continue

#3 Studentul intrudce requestul
    stillRunning = True
    while(stillRunning):
        # Send a request to the server
        request = input(requestMessage)
        s.send(request.encode())

        # Receive data from the server
        response = s.recv(1024).decode()

        if isinstance(response, str):
            # O exceptie care nu e gestionata explicit
            if response == Config.unhandeledExceptionOccured:
                print(Config.unhandeledExceptionOccured)
            # Input prea scurt / lung
            if response ==  Config.tooShortLongRequest:
                print(Config.tooShortLongRequest)
                continue
            # Request scris gresit
            if response == Config.badRequestIndex0:
                print(Config.badRequestIndex0)
            if response == Config.badRequestIndex1:
                print(Config.badRequestIndex1)
            if response == Config.badRequestIndex2:
                print(Config.badRequestIndex2)

            print(Config.tryAgain)
            continue



        # Everything is good, let's deserialize given json formatted stirng
        deserializedResponse = json.loads(response)

        # Print the response
        for day, schedule in deserializedResponse.items():
            for hour, class_info in schedule.items():
                print(f"{day} - {hour} : {class_info} : {schedule}")

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





#modific tot json ul
#
