import socket
import re

"""set up all the pattern"""

connec_req = re.compile("UTTT/1.0 CONNECTION [a-zA-Z1-9]*")
req_play = re.compile("UTTT/1.0 PLAY [0-8][0-8] [a-zA-Z1-9]*") #pattern of the request to say where the user play
req_state = re.compile("UTTT/1.0 NEW_STATE [a-zA-Z1-9]*")
req_ack = re.compile("UTTT/1.0 ACK")
req_end = re.compile("UTTT/1.0 END") #pattern of the packet that end the game
req_win = re.compile("UTTT/1.0 WIN (GUEST|HOST)?") 
state_req = re.compile("UTTT/1.0 404 STATE_PLAY [0-8][0-8] [a-zA-Z1-9]*") #the player receiving this packet cancels the last play and plays again
bad_req = re.compile("UTTT/1.0 405 BAD_REQUEST") #the player receiving this packet plays againr
fatal_err = re.compile("UTTT/1.0 406 FATAL_ERROR") #all other error that stops the game


"""Connection part"""

def connect_P1(ipc, portc, pseudo):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a new socket using the address familly (here AF_INET) and the socket type
    sock.bind((ipc, portc)) #bind the socket address
    sock.listen() #wait for a connection
    conn, addr = sock.accept() #accept the connection
    data = conn.recv(1024)
    ret = request_handling(data.decode())
    j = 0
    for i in range(2):
        match [ret[0], i, j]:
            case [0, _, 0]:
                j = 1
                i = 0
                name = ret[1]
                connection(conn, pseudo)
                data = conn.recv(1024)
                ret = request_handling(data.decode())
            case [1, _, 1]:
                return 0, name, ret[1:3], ret[3], conn
            case [5, _, _]:
                close(conn)
                return 4, ret[1], None, None, None
            case [-7, 0, _]:
                bad_request(conn)
                data = conn.recv(1024)
                ret = request_handling(data.decode())
            case _:
                fatal_error(conn)
                close(conn)
                return -6, None, None, None, None



def connect_P2(ipc, portc, ip, port, pseudo):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a new socket using the address familly (here AF_INET) and the socket type
    sock.bind((ip, port)) #bind the socket address
    sock.connect((ipc, portc)) #try to connect
    connection(sock, pseudo)
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range(2):
        match [ret[0], i]:
            case [0, _]:
                return 0, ret[1], sock
            case [5, _]:
                close(sock)
                return 5, ret[1], None
            case [-7, 0]:
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case _:
                fatal_error(sock)
                close(sock)
                return -6, None, None


"""Deconnection part"""

def close(sock):
    sock.close()


"""Communication part"""

def request_handling(request):
    ret = []
    if connec_req.match(request):
        ret.append(0)
        req_split = request.split('\n')[0].split(' ')
        ret.append(req_split[2])
        return ret
    elif req_play.match(request):
        ret.append(1)
        req_split = request.split('\n')[0].split(' ')
        ret.append(int(req_split[2][0]))
        ret.append(int(req_split[2][1]))
        ret.append(req_split[3])
        return ret
    elif req_state.match(request):
        ret.append(2)
        req_split = request.split('\n')[0].split(' ')
        ret.append(req_split[2])
        return ret
    elif req_ack.match(request):
        ret.append(3)
        return ret
    elif req_win.match(request):
        ret.append(4)
        req_split = request.split('\n')[0].split(' ')
        ret.append(req_split[2])
        return ret
    elif req_end.match(request):
        ret.append(5)
        return ret 
    elif state_req.match(request):
        req_split = request.split('\n')[0].split(' ')
        ret.append(-4)
        ret.append(int(req_split[2][0]))
        ret.append(int(req_split[2][1]))
        ret.append(req_split[3])
        return ret 
    elif bad_req.match(request):
        ret.append(-5)
        return ret
    elif fatal_err.match(request):
        ret.append(-6)
        return ret 
    else :
        ret.append(-7)
        return ret    

def connection (sock, pseudo):
    MESSAGE = f"UTTT/1.0 CONNECTION {pseudo}\n"
    sock.send(MESSAGE.encode())

def play(sock, num1, num2, h1):
    MESSAGE = f"UTTT/1.0 PLAY {num1}{num2} {h1}\n"
    sock.send(MESSAGE.encode())
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 2:
                return 0, ret[1]
            case 5:
                close(sock)
                return 5, ret[1]
            case -5:
                MESSAGE = f"UTTT/1.0 PLAY {num1}{num2} {h1}\n"
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6, None
            case _:  
                if i == 1:
                    fatal_error(sock)
                    close_player(sock)
                    return -6, None
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())

def new_state(sock, h2):
    MESSAGE = f"UTTT/1.0 NEW_STATE {h2}\n"
    sock.send(MESSAGE.encode())
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 3:
                return 0, None, None
            case 5:
                close(sock)
                return 5, None, None
            case -4:
                return -4, ret[1:3], ret[3]
            case -5:
                MESSAGE = f"UTTT/1.0 NEW_STATE {h2}\n"
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6
            case _:  
                if i == 1:
                    fatal_error(sock)
                    close_player(sock)
                    return -6
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())

def ack(sock):
    MESSAGE = f"UTTT/1.0 ACK\n"
    sock.send(MESSAGE.encode())
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 1:
                return 0, ret[1:3], ret[3]
            case 4:
                return 4, None, ret[1]
            case 5:
                close(sock)
                return 5, None, None
            case -5:
                MESSAGE = f"UTTT/1.0 ACK\n"
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6, None, None
            case _:  
                if i == 1:
                    fatal_error(sock)
                    close_player(sock)
                    return -6, None, None
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())

def win(sock, player):
    MESSAGE = f"UTTT/1.0 WIN {player}\n"
    sock.send(MESSAGE.encode())
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 5:
                close(sock)
                return 0
            case -5:
                MESSAGE = f"UTTT/1.0 WIN {player}\n"
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6
            case _:  
                if i == 1:
                    fatal_error(sock)
                    close_player(sock)
                    return -6
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())


def end(sock):
    MESSAGE = f"UTTT/1.0 END\n"
    sock.send(MESSAGE.encode())
    close(sock)
    return 0

"""Error part"""

def state_play(sock, num1, num2, h1):
    sock.send(f"UTTT/1.0 404 STATE_PLAY {num1}{num2} {h1}\n")
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 2:
                return 0, ret[1]
            case 5:
                close(sock)
                return 5, ret[1]
            case -5:
                MESSAGE = f"UTTT/1.0 404 STATE_PLAY {num1}{num2} {h1}n"
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6, None
            case _:  
                if i == 1:
                    fatal_error(sock)
                    close_player(sock)
                    return -7, None
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())

def bad_request(sock):
    sock.send(b"UTTT/1.0 405 BAD_REQUEST\n")

def fatal_error(sock):
    sock.send(b"UTTT/1.0 407 FATAL_ERROR\n")



if __name__ == "__main__":
    try:
        code, pseudo, move, h1, sock = connect_P1("localhost", 1235, "p1")
        print(code)
        print(pseudo)
        print(move[0])
        print(move[1])
        print(h1)
        import time 
        time.sleep(2)
        print("sleep")
        code, move, h1 = new_state(sock, "225")
        print(code)
        print("end")
    except BrokenPipeError:
        print("now")
    