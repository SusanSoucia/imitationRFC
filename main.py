from loglin import logDataBase
from potocol import *
from http import server
from socket import *
serverPort = 2525
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
online = logDataBase()
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Incoming Address:", addr)
    
    try:
        while True:  # 持续处理同一连接的多个消息
            sentence = connectionSocket.recv(1024).decode()
            if not sentence:  # 客户端关闭连接时，recv返回空字符串
                break
            
            print("Received:", sentence)
            handledMSG = handle(sentence, online)
            print("Response:", handledMSG)
            
            connectionSocket.send(handledMSG.encode())
    except ConnectionResetError:
        print(f"Client {addr} disconnected abruptly")
    finally:
        connectionSocket.close()