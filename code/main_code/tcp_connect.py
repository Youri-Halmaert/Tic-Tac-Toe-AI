import socket
import re
import hashlib

"""set up all the pattern"""
connec_req = re.compile("UTTT/1.0 CONNECTION [a-zA-Z1-9]*")
req_play = re.compile("UTTT/1.0 PLAY [0-8][0-8] [a-zA-Z0-9]*") #pattern of the request to say where the user play
req_state = re.compile("UTTT/1.0 NEW_STATE [a-zA-Z0-9]*")
req_ack = re.compile("UTTT/1.0 ACK")
req_end = re.compile("UTTT/1.0 END") #pattern of the packet that end the game
req_win = re.compile("UTTT/1.0 WIN( GUEST| HOST)?")
state_req = re.compile("UTTT/1.0 404 STATE_PLAY [0-8][0-8] [a-zA-Z0-9]*") #the player receiving this packet cancels the last play and plays again
bad_req = re.compile("UTTT/1.0 405 BAD_REQUEST") #the player receiving this packet plays againr
fatal_err = re.compile("UTTT/1.0 406 FATAL_ERROR") #all other error that stops the game

"""creation on the hash table"""

def hash_table(grid):
    m = hashlib.sha3_224()
    grid_to_hash = ""
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid_to_hash += grid[i][j]
        if (i % 3 == 2):
            if (i != 8):
                grid_to_hash += "/"
        else:
            grid_to_hash += "-"
    m.update(grid_to_hash.encode())
    return m.hexdigest()

"""Connection part"""

def connect_P1(ipc, portc, pseudo):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a new socket using the address familly (here AF_INET) and the socket type
    sock.bind(('', portc)) #bind the socket address
    sock.listen() #wait for a connection
    conn, addr = sock.accept() #accept the connection
    data = conn.recv(1024)
    ret = request_handling(data.decode())
    for i in range(2):
        match [ret[0], i]:
            case [0, _]:
                connection(conn, pseudo)
                return 0, ret[1], conn
            case [5, _]:
                close(conn)
                return 4, None, None
            case [-7, 0]:
                bad_request(conn)
                data = conn.recv(1024)
                ret = request_handling(data.decode())
            case _:
                fatal_error(conn)
                close(conn)
                return -6, None, None


def connect_P2(ip, port, pseudo):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a new socket using the address familly (here AF_INET) and the socket type
    sock.connect((ip, port)) #try to connect
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
        if len(req_split) > 2:
            ret.append(req_split[2])
        else:
            ret.append('')
        return ret
    elif req_end.match(request):
        ret.append(5)
        return ret
    elif state_req.match(request):
        req_split = request.split('\n')[0].split(' ')
        ret.append(-4)
        ret.append(int(req_split[3][0]))
        ret.append(int(req_split[3][1]))
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

def play(sock, num1, num2, grid, turn):
    h1 = hash_table(grid)
    MESSAGE = f"UTTT/1.0 PLAY {num1}{num2} {h1}\n"
    sock.send(MESSAGE.encode())
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    if turn:
        grid[num1][num2] = "0"
    else:
        grid[num1][num2] = "1"
    h2 = hash_table(grid)
    for i in range (2):
        match ret[0]:
            case 2:
                if h2 == ret[1]:
                    ack(sock)
                    return 0, grid
                else:
                    return state_play(sock, num1, num2, h1, h2), grid
            case 5:
                close(sock)
                return 5, None
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
                    close(sock)
                    return -6, None
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())

def new_state(sock, grid, pseudo, turn):
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 1:
                break
            case 5:
                close(sock)
                return 5, grid, pseudo
            case 4:
                return 4, None, None, None, pseudo
            case -5:
                if pseudo != None:
                    connection(sock, pseudo)
                    data = sock.recv(1024)
                    ret = request_handling(data.decode())
                    pseudo = None
                else:
                    ack()
                    data = sock.recv(1024)
                    ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6, grid, pseudo
            case _:
                if i == 1:
                    fatal_error(sock)
                    close(sock)
                    return -6, grid, pseudo
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())
    new_grid = grid
    big_game = ret[1]
    mini_game = ret[2]
    if turn:
        new_grid[big_game][mini_game] = "1"
    else:
        new_grid[big_game][mini_game] = "0"
    h2 = hash_table(new_grid)
    MESSAGE = f"UTTT/1.0 NEW_STATE {h2}\n"
    sock.send(MESSAGE.encode())
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 3:
                return 0, new_grid, big_game, mini_game, pseudo
            case 5:
                close(sock)
                return 5, None, None, None, pseudo
            case -4:
                i = -1
                new_grid = grid
                if turn:
                    new_grid[ret[1]][ret[2]] = "0"
                else:
                    new_grid[ret[1]][ret[2]] = "1"
                h2 = hash_table(new_grid)
                MESSAGE = f"UTTT/1.0 NEW_STATE {h2}\n"
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -5:
                MESSAGE = f"UTTT/1.0 NEW_STATE {h2}\n"
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6, None, None, None, pseudo
            case _:
                if i == 1:
                    fatal_error(sock)
                    close(sock)
                    return -6
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())

def ack(sock):
    MESSAGE = f"UTTT/1.0 ACK\n"
    sock.send(MESSAGE.encode())

def win(sock, player):
    if player == "p1_win":
        MESSAGE = f"UTTT/1.0 WIN GUEST\n"
    elif player == "p2_win":
        MESSAGE = f"UTTT/1.0 WIN HOST\n"
    else:
        MESSAGE = f"UTTT/1.0 WIN\n"
    sock.send(MESSAGE.encode())
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 5:
                close(sock)
                return 0
            case -5:
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6
            case _:
                if i == 1:
                    fatal_error(sock)
                    close(sock)
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

def state_play(sock, num1, num2, h1, h2):
    MESSAGE = f"UTTT/1.0 404 STATE_PLAY {num1}{num2} {h1}\n"
    sock.send(MESSAGE.encode())
    data = sock.recv(1024)
    ret = request_handling(data.decode())
    for i in range (2):
        match ret[0]:
            case 2:
                if ret[1] == h2:
                    return 0
                else:
                    fatal_error(sock)
                    close(sock)
                    return -7
            case 5:
                close(sock)
                return 5
            case -5:
                MESSAGE = f"UTTT/1.0 404 STATE_PLAY {num1}{num2} {h1}n"
                sock.send(MESSAGE.encode())
                data = sock.recv(1024)
                ret = request_handling(data.decode())
            case -6:
                close(sock)
                return -6
            case _:
                if i == 1:
                    fatal_error(sock)
                    close(sock)
                    return -7
                bad_request(sock)
                data = sock.recv(1024)
                ret = request_handling(data.decode())

def bad_request(sock):
    sock.send(b"UTTT/1.0 405 BAD_REQUEST\n")

def fatal_error(sock):
    sock.send(b"UTTT/1.0 407 FATAL_ERROR\n")



'''if __name__ == "__main__":
    print(hash_table(
  [
    ["0","1","0","1","0","1","1","0","1"],
    [".",".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".",".","."],

    ["0",".",".",".",".",".",".",".","1"],
    [".",".",".",".","1",".",".",".","."],
    [".",".",".",".",".",".",".",".","."],

    [".",".",".",".",".",".",".",".","."],
    [".",".",".",".","1",".",".",".","."],
    ["1",".",".",".","0",".",".",".","."],
  ]
))'''
    
