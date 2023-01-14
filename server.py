import json
import socket

# Load data from json file
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

requestMessage = "Enter a request.\ne.g:ANI/Grupa1/Subgrupa1\n"

while True:
    #1 Serverul asteapta comanda START
    while True:
        request = client.recv(1024).decode()
        if request.upper() == "START":
            #2 Serverul raspunde ca este pregatit de dialog
            client.send(requestMessage.encode())
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

            # Send to client that data was found, ask for day, send back all hours, ask for hour, send back all options
            # Send data back to client
            client.send(json.dumps(result).encode())

        except IndexError:
            result = Config.tooShortLongRequest
            client.send(result.encode())
        except ValueError:
            result = errorMessage
            client.send(result.encode())
        except BaseException:
            result = Config.unhandeledExceptionOccured
            client.send(result.encode())

# Close the connection with the client
client.close()
used_socket.close()
