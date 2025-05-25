from socket import *
import threading

def handle_client(connection_socket):
    try:
        message = connection_socket.recv(1024).decode()
        filename = message.split()[1]
        
        with open(filename[1:], 'r', encoding='utf-8') as f:
            outputdata = f.read()
        
        # Отправка заголовков
        headers = 'HTTP/1.1 200 OK\r\n'
        headers += 'Content-Type: text/html; charset=UTF-8\r\n\r\n'
        connection_socket.send(headers.encode('utf-8'))
        
        # Отправка содержимого
        connection_socket.send(outputdata.encode('utf-8'))
    
    except IOError:
        error_msg = 'HTTP/1.1 404 Not Found\r\n\r\n404 Not Found'
        connection_socket.send(error_msg.encode('utf-8'))
    
    finally:
        connection_socket.close()

# Основной поток сервера
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 8080))
serverSocket.listen(5)  # Увеличили очередь соединений

print('Сервер запущен...')

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f'Подключение от {addr}')
    
    # Запускаем новый поток для обработки запроса
    client_thread = threading.Thread(
        target=handle_client, 
        args=(connectionSocket,)
    )
    client_thread.start()
