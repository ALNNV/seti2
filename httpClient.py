import socket
import sys

def main():
    if len(sys.argv) != 4:
        print("Использование: httpClient.py <хост> <порт> <файл>")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
    
    # HTTP-запрос
    request = (
        f"GET {path} HTTP/1.0\r\n"
        f"Host: {host}\r\n"
        "Connection: close\r\n\r\n"
    )
    
    try:
        # сокет и подклюбчение
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(5)
            client_socket.connect((host, port))
            
            print(f"Отправляемый запрос:\n{request}\n")
            client_socket.sendall(request.encode('utf-8'))
            
            response = b''
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                response += data
            
            print(response.decode('utf-8', errors='ignore'))
    
    except Exception as e:
        print(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    main()
