import zmq

context = zmq.Context()
print("Client attempting to connect to server...")

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
    outgoing = input("> ")
    socket.send_string(outgoing)
    message = socket.recv_string()
    f = open("clientlog.txt", mode="a", encoding="utf-8")
    print(f"Server sent back: {message}")
    f.write(message + "\n")
    f.close()


