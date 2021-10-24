# coding: utf-8
# author: myc

import re
import socket
import argparse


def make_command(string):
    command = '*'
    command_list = string.split()
    command += str(len(command_list)) + '\r\n'
    for cmd in command_list:
        command += '$' + str(len(cmd)) + '\r\n' + cmd + '\r\n'
    return command


def parse_output(string):
    if string.startswith('*') or string.startswith('$'):
        return re.sub("(\*\d+\\r\\n)?\$\d+\\r\\n", "", string)
    return string


def connect_redis(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(1)
        sock.connect((host, int(port)))
        while True:
            command = input('>')
            if command == "":
                continue
            if command == "exit":
                print("Bye ~\n")
                break
            command = make_command(command)
            sock.send(command.encode('utf-8'))
            data = ""
            while True:
                _ = sock.recv(1024)
                data += _.decode('utf-8')
                if len(_) < 1024:
                    break
            print(parse_output(data))
    except Exception as e:
        print(e)
    finally:
        sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='redis-cli')
    parser.add_argument('--host', dest='host', default='127.0.0.1', help='redis host')
    parser.add_argument('-p', dest='port', default=6379, help='redis port')
    args = parser.parse_args()
    connect_redis(args.host, args.port)
