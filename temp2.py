import os
import sys
import chardet
from socket import *

PORT = int(sys.argv[1])
print("Student ID   :   20192806")
print("Name         :   Han Byeong Kyu")

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost', PORT))
serverSocket.listen()



while True:
    conn, addr = serverSocket.accept()
    recv = conn.recv(2048)
    encoding = chardet.detect(recv)['encoding']

    byte_string = b""

    print(f"encoding : {encoding}, byte_string : {byte_string}")
    if encoding:
        sentence = recv.decode('utf-8').split(' ')
        split_str = sentence[1].split('\n', 1)
        sentence[1:2] = split_str  
        operation = sentence[0].strip()     # PUT / GET ...
        file_name = sentence[1].strip()     # b.html ...

    else:
        byte_string += recv
        byte_code = byte_string.split(b'\n')[1]

        print(f"byte_string is : {byte_string}\nbyte_code is : {byte_code}")
        header = byte_string.split(b'\n')[0].decode()
        operation, file_name = header.split()
        print(f"operation : {operation}, file_name : {file_name}")
        
        sentence = byte_code.decode('utf-16-le').split(' ')
        

        # operation = 
        

    split_str = sentence[1].split('\n', 1)
    sentence[1:2] = split_str  
    
    operation = sentence[0].strip()     # PUT / GET ...
    file_name = sentence[1].strip()     # b.html ...
    
    
    print(f"sentence is : {sentence}\nencoding is : {encoding}")
    print(f"file_name is : {file_name}\noperation is : {operation}")
    print("----------------------------------------------------")
    
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
            print("for문 입장")
            for i in range(2, len(sentence)):
                if i == len(sentence)-1:
                    print(f"it should be 'Fil' : {sentence[i]}")
                    i_byte = sentence[i].encode('utf-8')
                    file.write(i_byte)
                else:
                    sentence[i] += " "
                    i_byte = sentence[i].encode('utf-8')
                    file.write(i_byte)


            # for i in sentence[2:]:
            #     i += " "
            #     i_byte = i.encode('utf-8')
            #     file.write(i_byte)

            print("for문 탈출")
            while True:
                data = conn.recv(2048)
                if not data:
                    break
                file.write(data)
        # conn.send("File transfer complete.\r\n".encode())

    elif operation == "LS":
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.' + file_name)]
        if not files:
            # 해당 확장자의 파일이 없으면 "FILE NOT FOUND"을 클라이언트로 전송합니다.
            # conn.send("FILE NOT FOUND\r\n".encode())
            pass
        else:
            # 해당 확장자의 파일 목록을 클라이언트로 전송합니다.
            file_list = '\r\n'.join(files) + '\r\n'
            conn.send(file_list.encode('utf-8'))
    
    conn.close()
