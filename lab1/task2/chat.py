import socket
import threading

# Список клієнтів
clients = []

def handle_client(client_socket):
    while True:
        try:
            # Отримати дані від клієнта
            data = client_socket.recv(1024)
            
            # Перевірка чи отримано дані
            if not data:
                break

            # Відправити отримані дані всім клієнтам, крім відправника
            for client in clients:
                if client != client_socket:
                    client.send(data)
        except:
            # Обробка помилок при отриманні або відправці даних
            break

def main():
    server_ip = '127.0.0.1'
    server_port = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    print(f"Сервер слухає на {server_ip}:{server_port}")

    while True:
        # Прийняти з'єднання від клієнта
        client_socket, client_address = server_socket.accept()
        print(f"Новий клієнт підключився: {client_address}")

        # Додати клієнта до списку
        clients.append(client_socket)

        # Запустити окремий потік для обробки клієнта
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
