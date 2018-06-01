import serial
from time import sleep
from threading import Thread
import binascii

class SerialInterface():
    def __init__(self,args):
        self.args = args


    # 打开串口
    def open(self):
        # self.ser = serial.Serial('COM83', 115200, parity='N', timeout=0.5)
        self.ser = serial.Serial(self.args[0], self.args[1], parity=self.args[2],timeout=0.5)#, timeout=0.5
        self.ser.set_buffer_size(rx_size=15000)
        print(self.ser.name, self.ser.port)
        # self.ser.close()
        # self.ser.open()
        if self.ser.is_open:
            print('opened')
            return  True
        else:
            print('open failed')
            return False

    #关闭串口
    def close(self):
        self.ser = serial.Serial(self.args[0], self.args[1], parity=self.args[2], timeout=0.5)
        if self.ser.is_open:#如果串口已经打开
            self.ser.close()
            print('closed')
        else:
            pass

    # 发送一个字节
    def write(self,data,isHex=False):
        if isHex:
            data = binascii.unhexlify(data)
        self.ser.write(data)
        print(data)

    #读数据
    def read(self):
        self.readthread = Thread(target=self.alwaysread)
        self.readthread.setDaemon(True)
        self.readthread.start()
        s=self.alwaysread()
        return s

    def alwaysread(self):
        print('the receive buffer size is ',self.ser.in_waiting)

        s = self.ser.read(15000)
        r = s.hex()
        # print(r)

        r1=r[42:7317*2]
        result=[int(r1[i:i+4],16) for i in range(0,len(r1)) if  i%4==0]



        # print(r)

        return r

# si = SerialInterface()
# cmd0 = '83'.encode('ascii')
# cmd1 = '7D'.encode('utf-8')
# cmd2 = 'FF'.encode('utf-8')
# si.open()
# #开启循环读的线程
# si.read()
# si.write(b'S')
# # si.write(cmd1)
# # si.write(cmd2)
# sleep(1)

