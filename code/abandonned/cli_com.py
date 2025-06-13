import sys
import tcp_connect as comm
import os

def student_client(argv, sock):
    if len(argv) <=1:
        while True:
                userStr = input()
                ret = make_cmd(userStr, sock)
                if ret == 0 or ret == 1:
                    return ret
    else :
        for i in range(1, len(argv)):
            try:
                with open(argv[i], 'r') as file:
                    list_cmd = file.read()
            except IOError:
                print(f"Could not open the file {analyze_str}")
                return 0

            # execute all the command in the file
            cmd_list = list_cmd.split('\n')
            for cmd in cmd_list:
                ret = make_cmd(cmd, sock)
                if ret == 0 or ret == 1:
                    return ret
            return 0

    return 0


def make_cmd (cmd, sock):
    match cmd.split(' '):
        case [connect, pseudo]:
            comm.connection(sock, pseudo)
        case [play, num1, num2]:
            comm.play(sock num1, num2)
        case [win, player]:
            comm.win(sock, player)
        case [end]:
            comm.end(sock)
        case [close]:
            return 0
        case other:
            
            

if __name__ == "__main__":
    student_client(sys.argv)