import socket

HOST = '127.0.0.1'
PORT = 8888

data = '{"latitude": 9999.7128, "longitude": -84.0060, "timestamp": "2023-05-01T12:00:00", "device_id": 1}'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(data.encode())
    response = s.recv(1024)

print('Received', response.decode())
