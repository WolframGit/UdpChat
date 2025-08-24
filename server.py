import socket
import platform
import json
import os
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
        print('Некорректно введен IPv4...')
        server(str(input('Введите ваш IPv4 -> ')))

def server(host, port: int = 8000):
    try:
        if not host_validate(host):
            print('Некорректно введен IPv4...')
        
        pass
    except KeyboardInterrupt:
        print('Выход...')
    clear_terminal()

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    users = []
    users_nickname = {}

    print(f'Добро пожаловать на чат!\n')
    while True:
        try:
            msg, addr = server.recvfrom(UDP_MAX_SIZE)
            client_id = addr[1]

            if addr not in users:
                users.append(addr)

            if not msg:
                continue

            message = msg.decode('utf-8')
        
            try:
                data = json.loads(message)
                if data['type'] == 'response' and data['request_id'] == 'nickname':
                    new_nickname = data.get('nickname', f'User{addr[1]}')
                    users_nickname[client_id] = new_nickname
                    print(f'User{addr[1]} изменил никнейм на - {new_nickname}')
                    continue
            except json.JSONDecodeError:
                pass
        
            if message == '/join':
                print(f'Users{client_id} - Присоединился к чату!')
                continue

            if message == '/help':
                    help_text = 'Для установки никнейма - /nickname'
                    server.sendto(help_text.encode('utf-8'), addr)
                    continue
                
        
            if message == '/nickname':
                input_nickname = {
                    'type': 'input',
                    'prompt': 'Введите новый никнейм -> ',
                    'request_id': 'nickname'
                }
                response = json.dumps(input_nickname).encode('utf-8')
                server.sendto(response, addr)
                continue

            nickname = users_nickname.get(client_id, f'User{addr[1]}')
            formatted_msg = f'{nickname}: {message}'
            for user in users:
                if user != addr:
                    server.sendto(formatted_msg.encode('utf-8'), user)
        except KeyboardInterrupt:
            print('Произошла ошибка...\nВыход через 2 секунды.')
            s(2)

if __name__=='__main__':
    clear_terminal()
    server(str(input('Введиет ваш IPv4 -> ')))