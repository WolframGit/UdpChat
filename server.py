import socket
import platform
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
        print(f'Прослушивается {host}:{port}')
        while True:
            try:
                msg, addr = server.recvfrom(UDP_MAX_SIZE)

                if addr not in users:
                    users.append(addr)

                if not msg:
                    continue

                message = msg.decode('utf-8')
                client_id = addr[1]
                nickname = users_nickname.get(client_id, f'User{addr[1]}')

                if message == '/join':
                    print(f'{nickname} - присоединился к чату!')
                    continue

                if message == '/help':
                    help_text = '''\nПомощь:

        Для установки никнейма - /nickname [Новый никнейм]
        Выйти из чата - /leave\n'''
                    server.sendto(help_text.encode('utf-8'), addr)
                    continue
                
        
                if message.startswith('/nickname'):
                    rename = message.split()

                    if len(rename) != 2:
                        server.sendto(f'\nДанный никнейм не корректен! Повторите попытку...\n'.encode('utf-8'), addr)
                        continue
                    
                    new_nickname = rename[1]
                    if len(new_nickname) < 2 or len(new_nickname) > 15:
                        server.sendto(f'\nНикнейм должен быть меньше 2 символов и не более 15!\nПовторите попытку...\n'.encode('utf-8'), addr)
                        continue

                    old_nickname = nickname
                    if old_nickname == new_nickname:
                        server.sendto(f'{old_nickname} уже используется вами!'.encode('utf-8'), addr)
                        continue        
                    else:
                        users_nickname[client_id] = new_nickname
                        server.sendto(f'{old_nickname} был сменен на - {new_nickname}'.encode('utf-8'), addr)

                    notification = f'{old_nickname} сменил никнейм на - {new_nickname}'.encode('utf-8')
                    for user in users:
                        if user != addr:
                            server.sendto(notification, user)
                    

                formatted_msg = f'{nickname}: {message}'
                for user in users:
                    if user != addr:
                        server.sendto(formatted_msg.encode('utf-8'), user)
            except Exception as e:
                print(f'Ошибка: {e}')
                continue
    except KeyboardInterrupt:
        print('Произошла ошибка...\nВыход через 2 секунды.')
        s(2)
        clear_terminal()
        exit

if __name__=='__main__':
    clear_terminal()
    server(str(input('Введите IP для подключения -> ')))
