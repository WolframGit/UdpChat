import socket
import threading
import platform
import os
import json
from time import sleep as s

SYSTEM = platform.system()
UDP_MAX_SIZE = 65535

def clear_terminal():
    if SYSTEM == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def host_validate(ip):
    try:
        if socket.inet_aton(ip):
            return True
    except socket.error:
        print('IPv4 некорректный...')
        s(2)
        clear_terminal()
        client_started(str(input('Введите ваш IPv4 -> ')))

def listening_message(client: socket.socket, addr_server):
    while True:
        try:
            msg = client.recv(UDP_MAX_SIZE)

            try:
                data = json.loads(msg.decode('utf-8'))
                if data['type'] == 'input' and data['request_id'] == 'nickname':
                    user_input_nickname = input(data['prompt'])

                    response = {
                        'type': 'response',
                        'request_id': 'nickname',
                        'nickname': user_input_nickname
                    }
                    client.sendto(json.dumps(response).encode('utf-8'), addr_server)
                    print(f'Твой никнейм изменен на - {user_input_nickname}')
                    continue
            except json.JSONDecodeError:
                pass
            
            print(f'\r\r{msg.decode('utf-8')}\nYou: ', end='')
        except Exception as e:
            print(f'\r\rПроизошла ошибка при получении сообщения: {e}\nYou: ', end='')

def client_started(host, port: int = 8000):
    try:
        if not host_validate(host):
            client_started(str(input('Введите ваш IPv4 -> ')))
        
        pass
    except Exception as e:
        print(f'Произошла ошибка... - {e}')
    clear_terminal()

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr_server = (host, port)

    client.sendto('/join'.encode('utf-8'), addr_server)
    print(f'Напишите /help, чтобы увидеть все команды!')

    threading.Thread(target=listening_message, args=(client, addr_server), daemon=True).start()

    while True:
        try:
            msg = input(f'You: ')
            client.sendto(msg.encode('utf-8'), addr_server)
        except KeyboardInterrupt:
            print(f'Произошла ошибка...\nВыход через 2 секунды.')
            s(2)


if __name__=='__main__':
    clear_terminal()
    client_started(str(input('Введите ваш IPv4 -> ')))