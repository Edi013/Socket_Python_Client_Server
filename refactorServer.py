import json
import socket

# Load data from json file
import traceback

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

while True:
    #1 Dialog 1 - START / STOP
    userWantsToStop = False
    while True:
        request = client.recv(1024).decode()
        if request.upper() == "START":
            print("One client requested START")
            break
        if request.upper() == "STOP":
            print("One client requested STOP")
            userWantsToStop = True
            break
    if userWantsToStop == True:
        break


    #2 Dialog 2 - REQ 1
    result = data
    while True:
        # send req1
        client.send(Config.request1Message.encode())
        requestProcessedSent = False
        while True:
            try:
                kth = 0
                errorMessage = "errorMessage initialization"
                # Read data from the client
                request = client.recv(1024).decode().split("/")
                if (len(request) > 3):
                    raise IndexError
                years = ["ANI", "ANII", "ANIII", "ANIMASTER", "ANIIMASTER"]
                groups = ["Grupa1", "Grupa2"]
                subgroups = ["Subgrupa1", "Subgrupa2"]
                wrong = False
                for identifier in request:
                    #existsInJson = result.get(identifier, False)
                    #if not existsInJson:
                    if kth == 0:
                        if identifier not in years:
                            errorMessage = Config.badRequestIndex0
                            wrong = True
                    if kth == 1:
                        if identifier not in groups:
                            errorMessage = Config.badRequestIndex1
                            wrong = True
                    if kth == 2:
                        if identifier not in subgroups:
                            errorMessage = Config.badRequestIndex2
                            wrong = True
                    if wrong:
                        raise ValueError(errorMessage)
                    # noinspection PyTypeChecker
                    result = result[identifier]
                    kth += 1
                client.send(Config.requestProcessed.encode())
                requestProcessedSent = True
                break
            except IndexError as e:
                result = Config.tooLongRequest
                client.send(result.encode())
                print(e)

            except ValueError as e:
                result = str(e)
                client.send(result.encode())
                print(e)

        if requestProcessedSent:
            break


    #3 Dialog 3 - REQ 2
    while True:
        client.send(Config.request2Message.encode())
        requestProcessedSent = False
        requestHaveOptions = False
        #primeste req si verifica pana cand inputul e bun
        while True:
            try:
                request = client.recv(1024).decode().split("/")

                #day
                days = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]
                day = request[0]

                if day not in days:
                    raise BlockingIOError
                #options
                if len(request) > 1:
                    requestHaveOptions = True
                    options = ["DM", "TM", "P", "S"]
                    for i in range(1, len(request)):
                        if request[i] not in options:
                            raise AssertionError

                # noinspection PyTypeChecker
                result = result[request[0]]
                client.send(Config.requestProcessed.encode())
                requestProcessedSent = True
                break
            except AssertionError:
                result = Config.invalidOptionInput
                client.send(Config.invalidOptionInput.encode())
                continue
            except BlockingIOError:
                result = Config.invalidDayInput
                client.send(result.encode())
                continue
        if requestProcessedSent:
           break


    #aici
    #process send response to display
    print(result)
        # noinspection PyTypeChecker

    if not requestHaveOptions:
        client.send(json.dumps(result).encode())
    elif requestHaveOptions:
        hours = []
        detailsToSend = {}
        for hour in result:
            hours.append(hour)
            print("hour")
            print(hour)
    # noinspection PyTypeChecker
            details = result[hour]
            for detail in details:
                if detail in request:
                    print("option")
                    print(detail)
                    print("option value")
                        # noinspection PyTypeChecker
                    print(details[detail])
                                        # noinspection PyTypeChecker
                    detailsToSend[detail] = details[detail]
        client.send(json.dumps(hours).encode())
        client.send(json.dumps(detailsToSend).encode())


print("No client is online")
print("Shutting down ...")
# Close the connection with the client
used_socket.close()
