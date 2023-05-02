import os
import sys
from socket import *

PORT = int(sys.argv[1])
print("Student ID   :   20192806")
print("Name         :   Han Byeong Kyu")

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', PORT))
serverSocket.listen()

while True:
    conn, addr = serverSocket.accept()
    recv = conn.recv(2048)
    byte_string = b""
    encoding = None

    try:
        encoding = 'utf-8'
        sentence = recv.decode('utf-8').split(' ')
        split_str = sentence[1].split('\n', 1)
        sentence[1:2] = split_str  
        operation = sentence[0].strip()     # PUT / GET ...
        file_name = sentence[1].strip()     # b.html ...
        print(f"operation is : {operation}, file_name is : {file_name}")
    except UnicodeDecodeError:
        byte_code = b""
        recv_split = recv.split(b'\n')[1:]
        for i in range(len(recv_split)):
            if i == len(recv_split)-1:
                byte_code += recv_split[i]
            else:
                byte_code += recv_split[i] + b"\n"
        header = recv.split(b'\n')[0].decode()
        operation, file_name = header.split()
        encoding = 'utf-16-le'


    

    if operation == "GET":
        if not os.path.exists(file_name):
            # 파일이 존재하지 않으면 FILE NOT FOUND
            conn.send("FILE NOT FOUND\r\n".encode())
        else:
            # 존재하면 파일 전송
            with open(file_name, "rb") as file:
                content = file.read()
                conn.send(content)

    elif operation == "PUT":
        with open(file_name, "wb") as file:
            if encoding == "utf-8":
                for i in range(2, len(sentence)):
                    if i == len(sentence)-1:
                        i_byte = sentence[i].encode('utf-8')
                        file.write(i_byte)
                    else:
                        sentence[i] += " "
                        i_byte = sentence[i].encode('utf-8')
                        file.write(i_byte)
            else:
                file.write(byte_code)
 
            while True:
                data = conn.recv(2048)
                if not data:
                    break
                file.write(data)
        

    elif operation == "LS":
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.' + file_name)]
        if not files:
            # 해당 확장자의 파일이 없으면 "FILE NOT FOUND"을 클라이언트로 전송합니다.
            # conn.send("FILE NOT FOUND\r\n".encode())
            pass
        else:
            # 해당 확장자의 파일 목록을 클라이언트로 전송합니다.
            # file_plus_rn = [i + "\r\n" for i in files]
            # result = ""
            # for i in file_plus_rn:
            #     result += i
            file_list = '\r\n'.join(files) + '\r\n'
            conn.send(file_list.encode())

    conn.close()
