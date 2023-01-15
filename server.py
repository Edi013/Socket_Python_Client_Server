import json
import socket

# Load data from json file
import traceback

from Exceptions import IncorrectInputException
from config import Config

def isConnectionAvailable(response):
    if response == b'':
        return False
    return True

with open("data.json", "r") as jsonFile:
    data = json.load(jsonFile)

# Create a socket object
used_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific address and port
used_socket.bind(("localhost", 12121))
# Listen for incoming connections
used_socket.listen(5)


while True:
    # Establish a connection with the client
    clientSocket, client_addres = used_socket.accept()
    print(f"Got connection from {client_addres}")
    connectionAvailable = True

    #1 Serverul asteapta comanda START
    while connectionAvailable:
        request = clientSocket.recv(1024).decode()
        if(not isConnectionAvailable(request)):
            connectionAvailable = False
            break

        if request.upper() == "START":
            #2 Serverul raspunde ca este pregatit de dialog
            print("One client requested start")
            connectionAvailable = True
            break
        if request.upper() == "STOP":
            print("One client requested stop" + client_addres)
            connectionAvailable = False
            break

    # 3 Serverul asteapta interogare corect formulata despre orar
    while connectionAvailable:
        try:
        # 3.1 Cere si primeste  request 1
                # Primul request An/Grupa/Subgrupa
            clientSocket.send(Config.request1Message.encode())
            # Read data from the client
            request = clientSocket.recv(1024).decode().split("/")
            if(not isConnectionAvailable(request)):
                connectionAvailable = False
                break

    # 4 Serverul verifica validitatea requestului
            if (len(request) > 3):
                raise IndexError

            result = data
            kth = 0
            errorMessage = "errorMessage initialization"
        # Verificam daca requestul are sintaxa valida
        # Timitem mesaj daca are sau nu.
            for identifier in request:
                existsInJson = result.get(identifier, False)
                if existsInJson == False:
                    if kth == 0:
                        errorMessage = Config.badRequestIndex0
                    if kth == 1:
                        errorMessage = Config.badRequestIndex1
                    if kth == 2:
                        errorMessage = Config.badRequestIndex2
                    raise ValueError
                result = result[identifier]
                kth+=1
            # Send data back to client
            clientSocket.send(Config.requestProcessed.encode())

            # 2nd request is awaited
            #receive req2
            request = clientSocket.recv(1024).decode().split("/")
            if(not isConnectionAvailable(request)):
                connectionAvailable = False
                break

            # Mereu avem argumentul 0, verificam daca e valid
            ok = False
            for day in ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]:
                if request[0] == day:
                    ok = True
            if not ok:
                raise BlockingIOError

            for input_option in request:
                if input_option == request[0]:
                    continue
                ok = False
                for good_option in ["DM", "TM", "P", "S"]:
                    if input_option == good_option:
                        ok = True
                    if not ok:
                        raise AssertionError

            clientSocket.send(Config.requestProcessed.encode())

            result_save = result = result[request[0]]
            # Daca nu a fost folosita nicio optiune / detaliu, se considera a fi dorite toate
            if len(request) != 1:
                toPrint = {}
                hours = []
                for hour in result:
                   hours.append(hour)
                   aux = result[hour]
                   for value in aux:
                       if value in request:
                           toPrint[value] = aux[value]
                           print(toPrint)
                           print(type(toPrint))
                clientSocket.send(json.dumps(hours).encode())
                clientSocket.send(json.dumps(toPrint).encode())
            else:
                clientSocket.send(json.dumps(result_save).encode())

         # Ask for next operation
            userContinuesOrNot = clientSocket.recv(1024).decode()
            if(not isConnectionAvailable(userContinuesOrNot)):
                connectionAvailable = False
                break
            if userContinuesOrNot == 'Y':
                connectionAvailable = True
            elif userContinuesOrNot == 'N':
                connectionAvailable = False
            else:
                connectionAvailable = False
                print("Unexpected error line 141 server side !")


        except AssertionError:
            result = Config.invalidOptionInput
            clientSocket.send(result.encode())
        except BlockingIOError:
            result = Config.invalidDayInput
            clientSocket.send(result.encode())
        except IndexError:
            result = Config.tooLongRequest
            clientSocket.send(result.encode())
        except ValueError as e:
            result = errorMessage
            clientSocket.send(result.encode())
        except BaseException as e:
            result = Config.unhandeledExceptionOccured
            clientSocket.send(result.encode())
    clientSocket.close()


print("No client is online")
print("Shutting down ...")
# Close the connection with the client
used_socket.close()



