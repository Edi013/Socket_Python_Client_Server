import json
import socket

# Load data from json file
import traceback

from Exceptions import IncorrectInputException
from config import Config


with open("data.json", "r") as jsonFile:
    data = json.load(jsonFile)

def isConnectionAvailable(response):
    if response == b'':
        return False
    return True


# Create a socket object
used_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
used_socket.bind(("localhost", 12121))

# Listen for incoming connections
used_socket.listen(5)

# Establish a connection with the client
client, client_addres = used_socket.accept()
print(f"Got connection from {client_addres}")

connectionAvailable = False
while True:
    #1 Serverul asteapta comanda START
    while True:
        request = client.recv(1024).decode()
        #connectionAvailable = isConnectionAvailable(request)

        if request.upper() == "START":
            #2 Serverul raspunde ca este pregatit de dialog
            client.send(Config.request1Message.encode())
            print("One client requested start")
            connectionAvailable = True
            break
        if request.upper() == "STOP":
            print("One client requested stop")
            connectionAvailable = False
            break

    # 3 Serverul asteapta interogare corect formulata despre orar
    while connectionAvailable:
        try:
            # Read data from the client
            request = client.recv(1024).decode().split("/")
            connectionAvailable = isConnectionAvailable(request)

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
            connectionAvailable = isConnectionAvailable(request)

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



            result_save = result = result[request[0]]

            # Daca nu a fost folosita nicio optiune / detaliu, se considera a fi dorite toate

            if len(request) != 1:
                toPrint = {}
                hours = []
                for hour in result:
                   print("o iteratie in hour in result linia 116")
                   hours.append(hour)
                   aux = result[hour]
                   for value in aux:
                       if value in request:
                           toPrint[value] = aux[value]
                           print(toPrint)
                           print(type(toPrint))
                client.send(json.dumps(hours).encode())
                client.send(json.dumps(toPrint).encode())
            else:
                client.send(json.dumps(result_save).encode())

        # Ask for next operation
            userContinuesOrNot = client.recv(1024).decode()
            if(not isConnectionAvailable(userContinuesOrNot)):
                connectionAvailable = False
                break
            if userContinuesOrNot == 'Y':
                connectionAvailable = True
                print("Y was inputed")
            elif userContinuesOrNot == 'N':
                print("N was inputed")
                connectionAvailable = False
                break
            else:
                connectionAvailable = False
                print("Unexpected error line 141 server side !")
                break

        except AssertionError:
            result = Config.invalidOptionInput
            client.send(Config.invalidOptionInput.encode())
        except BlockingIOError:
            result = Config.invalidDayInput
            client.send(result.encode())
        except IndexError:
            result = Config.tooLongRequest
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

print("No client is online")
print("Shutting down ...")
# Close the connection with the client
client.close()
used_socket.close()



