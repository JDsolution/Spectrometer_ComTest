#ok，现在可以开始我的python开发了
#像素数据模型
#具有字节长度，切片后的像素数据等属性
import random

class PixelUtil():


    # def getpixelresult(self,raw):
    #     self.r1 = raw[42:7317 * 2]
    #     self.length = len(self.r1)
    #     self.pixelresult = [int(self.r1[i:i + 4], 16) for i in range(0, len(self.r1)) if i % 4 == 0]
    #     return self.pixelresult

    def getstatusresult(self,raw):
        self.r1 = raw[42:7317 * 2]
        length = len(self.r1)
        pixelresult = [int(self.r1[i:i + 4], 16) for i in range(0, len(self.r1)) if i % 4 == 0]
        errornum = 0
        maxV = max(pixelresult)
        minV = min(pixelresult)
        received = len(raw)/2
        received2=int(received)
        pixels = len(pixelresult)
        return ['Glit',errornum,maxV,minV,received2,pixels]

    def getdemoresult(self):
        dr = []
        for i in range(0,3648):
            a = 10000+6000*random.random()+3000*random.random()
            dr.append(int(a))
        return dr


# pu = PixelUtil()
# r = pu.getdemoresult()
# print(r)