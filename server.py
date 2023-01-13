import json
import socket

# Load data from json file
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
    try:
        # Read data from the client
        request = client.recv(1024).decode().split("/")

        # Lookup the data in the json file
        result = data
        for identifier in request:
            existsInJson = result.get(identifier, False)
            if existsInJson == False:
                raise ValueError
            result = result[identifier]

        # Send data back to cliend
        client.send(json.dumps(result).encode())
    except ValueError:
        result = f"A value does not exits in the scheduale!"
        client.send(result.encode())
    except BaseException:
        result = "Exception occured"
        client.send(result.encode())

# Close the connection with the client
client.close()
used_socket.close()
