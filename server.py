import json
import socket

# Load data from json file
with open("scheduale", "r") as jsonFile:
    data = json.load(jsonFile)

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
s.bind(("localhost", 12121))

# Listen for incoming connections
s.listen(5)

# Establish a connection with the client
client, client_addres = s.accept()
print(f"Got connection from {client_addres}")

while True:
    try:
        # Read data from the client
        request = client.recv(1024).decode().split("/")

        # Lookup the data in the json file
        result = data
        for part in request:
            existsInJson = result.get(part, False)
            if existsInJson == False:
                raise ValueError
                break
            result = result[part]

        # Send data back to cliend
        c.send(json.dumps(result).encode())

    except ValueError:
        result = f"A value does not exits in the scheduale!"
        c.send(result.encode())
    except BaseException:
        result = "Exception occured"
        c.send(result.encode())

# Close the connection with the client
c.close()
s.close()
