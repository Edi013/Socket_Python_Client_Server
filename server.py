import json
import socket

# Load data from json file
import traceback

from Exceptions import IncorrectInputException
from config import Config

with open("data.json", "r") as jsonFile:
    data = json.load(jsonFile)

# Create a socket object
used_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
used_socket.bind(("localhost", 12121))

# Listen for incoming connections
used_socket.listen(5)

# Establish a connection with the client
client, client_addres = used_socket.accept()
print(f"Got connection from {client_addres}")

while True:
    #1 Serverul asteapta comanda START
    while True:
        request = client.recv(1024).decode()
        if request.upper() == "START":
            #2 Serverul raspunde ca este pregatit de dialog
            client.send(Config.request1Message.encode())
            break

    # 3 Serverul asteapta interogare corect formulata despre orar
    while True:
        try:
            # Read data from the client
            request = client.recv(1024).decode().split("/")

        #Primul request An/Grupa/Subgrupa
    # 4 Serverul verifica validitatea requestului

            # Manage the request
            if (len(request) > 3):
                raise IndexError

            result = data
            kth = 0
            errorMessage = "initializare ca nu ma lasa sa fac nimic fara"
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
            client.send(Config.requestProcessed.encode())

            # 2nd request is awaited
            #receive req2
            request = client.recv(1024).decode().split("/")

            # Mereu avem argumentul 0, verificam daca e valid
            if request[0] not in ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]:
                raise BlockingIOError

            jsonToString = result = result[request[0]]

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
                           print("val" + value +", aux[value]" + aux[value])
                           print(toPrint)
                           print(type(toPrint))
                client.send(json.dumps(hours).encode())
                client.send(json.dumps(toPrint).encode())
            else:
                client.send(json.dumps(jsonToString).encode())

        except BlockingIOError:
            result = Config.dataNotFound
            client.send(result.encode())
        except IndexError:
            result = Config.tooShortLongRequest
            client.send(result.encode())
        except ValueError as e:
            result = errorMessage
            client.send(result.encode())
            print("Caught an exception:")
            print(e)
            stack_trace = traceback.format_exc()
            print(stack_trace)
        except BaseException as e:
            result = Config.unhandeledExceptionOccured
            client.send(result.encode())
            print("Caught an exception:")
            print(e)
            stack_trace = traceback.format_exc()
            print(stack_trace)



# Close the connection with the client
client.close()
used_socket.close()


