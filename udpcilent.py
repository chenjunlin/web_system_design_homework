from socket import *
from time import ctime

host = '' #监听所有的ip
port = 13141 #接口必须一致
bufsize = 1024
addr = (host,port) 

udpServer = socket(AF_INET,SOCK_DGRAM)
udpServer.bind(addr) #开始监听

while True:

    data,addr = udpServer.recvfrom(bufsize)  #接收数据和返回地址
    data=data.decode()  
    print('分公司请注意，有新建订单，请对应分公司联系发货人',data)

udpServer.close()
