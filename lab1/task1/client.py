import socket

server_ip = '127.0.0.1'
server_port = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_ip, server_port))
    print(f"Підключено до сервера {server_ip}:{server_port}")

    while True:
        message = input("Введіть текст для сервера (або 'exit' для виходу): ")
        client_socket.send(message.encode('utf-8'))

        if message.lower() == 'exit':
            break

except ConnectionRefusedError:
    print(f"Помилка підключення: сервер {server_ip}:{server_port} не доступний.")

finally:
    client_socket.close()
