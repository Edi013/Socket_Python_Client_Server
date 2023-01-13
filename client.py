import socket
import json

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect(("localhost", 12121))

stillRunning = True
while(stillRunning):
    # Send a request to the server
    request = input("Enter a request, it should look like:\ne.g:ANI/Grupa1/Subgrupa1\n")
    s.send(request.encode())

    # Receive data from the server
    response = s.recv(1024).decode()

    if isinstance(response, str):
        # O exceptie care nu e gestionata explicit
        if response == "Exception occured":
            print("Something went wrong.\nIf you are sure that your input was good, it is a server problem!")
            continue
        # Input incorect
        if response == "A value does not exits in the scheduale!":
            print("A value does not exits in the scheduale!")
            print("Try again!")
            continue
        if response ==  "Invalid request":
            print("Invalid input was detected.")
            print("Try again!")
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




