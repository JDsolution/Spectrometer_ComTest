import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from pylab import show,plot
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from numpy import arange
from threading import Thread
import random
from time import sleep
from matplotlib import table
import ctypes
from ctypes.wintypes import LPCSTR
from comtest import serialInterface
from comtest import pixelUtil

PADX_G = 5
PADY_G = 5

class mainUI():
    #初始化
    def __init__(self):
        self.runflag = False
        self.demoflag = False
        self.openflag = False
        self.win = tk.Tk()
        self.win.protocol('WM_DELETE_WINDOW',self.closeWindow)
        self.win.title('ComTest')
        self.win.iconbitmap('pyc.ico')
        self.win.geometry('860x570+100+50')
        self.win.resizable(False,False)
        #创建widghtes
        self.createWidgets()
        #循环绘制图形
        self.drawdata()
        #创建状态栏
        self.drawtable()
        #创建像素处理工具类
        self.pixeltool = pixelUtil.PixelUtil()

    def closeWindow(self):
        self.win.destroy()
        try:
            self.SI.close()
        except:
            print("you haven't created self.SI yet")

    def createWidgets(self):
        global PADX_G
        global PADY_G
        #创建top frame容器
        self.top = ttk.LabelFrame(self.win)#text='top frame'
        self.top.grid(column=0,row=0,padx=10,pady=20)
        #创建mid frame容器
        self.mid = ttk.LabelFrame(self.win,text='mid frame')
        self.mid.grid(column=1,row=1)
        # self.run = tk.Button(self.win,text='Run')
        # self.run.grid(column=3,row=0)
        #创建串口号label
        self.uartnumlabel = tk.Label(self.top,text='串口号:')
        self.uartnumlabel.grid(column=0,row=0)
        # 创建串口号输入框
        self.uartnum = tk.IntVar()
        self.uartnumbox = ttk.Entry(self.top, textvariable=self.uartnum,width=10)
        self.uartnumbox.grid(column=1, row=0)
        self.uartnum.set('COM83')
        #创建波特率label
        self.baudratelabel = tk.Label(self.top,text='波特率:')
        self.baudratelabel.grid(column=0,row=1)
        #创建波特率复选框
        self.baud = tk.StringVar()
        self.baudratecombo = ttk.Combobox(self.top,values=(9600,13400,57600,115200,460800),width=8,textvariable=self.baud,state='readonly')
        self.baudratecombo.grid(column=1,row=1)
        self.baudratecombo.current(3)
        # print(self.baud,self.baudratecombo.get())
        # 创建更改波特率按钮
        self.changebaudbtn = ttk.Button(self.top, text='更改波特率')
        self.changebaudbtn.grid(column=2, row=1,padx=0)
        #创建校验位lable
        self.checkbitlabel = tk.Label(self.top,text='检校位:')
        self.checkbitlabel.grid(column=0,row=2)
        #校验位复选框
        self.checkbit = tk.StringVar()
        self.checkbitcombo = ttk.Combobox(self.top,values=('ODD','EVEN','NONE'),width=8,state='readonly')
        self.checkbitcombo.grid(column=1,row=2)
        self.checkbitcombo.current(2)

        #创建打开按钮
        self.openbtn = ttk.Button(self.top,text='打开',width=4,command=self.openuart)
        self.openbtn.grid(column=2,row=0,sticky='W',padx=PADX_G)

        #创建运行按钮
        style = ttk.Style()
        style.map("C.TButton",foreground=[('pressed','red'),('active','blue')],
                                        background=[('pressed','!disabled','black'),('active','white')]
                 )
        self.runbtntext = '运行'
        self.run = ttk.Button(self.top,text=self.runbtntext,width=10,style="C.TButton",command=self.pixel_sample)
        self.run.grid(column=3,row=0,padx=PADX_G,ipady=30,rowspan=8,columnspan=8,sticky='W')

        #创建演示按钮
        self.demobtntext = '演示'
        self.run = ttk.Button(self.top, text=self.demobtntext, width=10, style="C.TButton",command=self.demobtnclicked)
        self.run.grid(column=13, row=0, padx=PADX_G, ipady=30, rowspan=8, columnspan=8, sticky='W')

        #积分label
        self.intglabel = ttk.Label(self.top,text='积分  ：')
        self.intglabel.grid(column=11,row=0,padx=PADY_G,sticky='W')
        #设置积分框
        self.intg = tk.IntVar()
        self.intgentry = tk.Entry(self.top,textvariable=self.intg,width=10,borderwidth=1)
        self.intgentry.grid(column=12,row=0,padx=PADY_G)
        #当前积分label
        self.currentlabel = tk.Label(self.top,text='当前积分：')
        self.currentlabel.grid(column=11,row=1,padx=PADX_G,sticky='W')
        #当前积分输入框
        self.currententry = tk.Entry(self.top,text='0',width=10,borderwidth=1,state='readonly')
        self.currententry.grid(column=12,row=1,padx=PADX_G)
        #采集延时label
        self.latencylabel = tk.Label(self.top,text='采集延时：')
        self.latencylabel.grid(column=11,row=2,padx=PADX_G,sticky='W')
        #采集延时输入框
        self.latency = tk.StringVar()
        self.latencyentry = tk.Entry(self.top,textvariable=self.latency,width=10,borderwidth=1)
        self.latencyentry.grid(column=12,row=2,padx=PADX_G)
        self.latency.set('1500')

    # 创建表格
    def drawtable(self):
        self.table_text = ('Type','errors','max','min','received','pixels')
        self.treetable = ttk.Treeview(self.top,height=1,show='headings',columns=self.table_text)
        for i in range(0,6):
            self.treetable.column(self.table_text[i], width=100, anchor='center')
        for i in range(0,6):
            self.treetable.heading(self.table_text[i], text=self.table_text[i])
        self.treetable.grid(column=0,row=15,columnspan=20,pady=5,padx=0,sticky='W')
        self.treetable.insert('', 0, values=('Glit', '0', '65535', '1000','7319','3648'))

    def drawdata(self):
        # 创建图表
        self.fig = Figure(figsize=(8.5, 3.5), facecolor='lightgray',tight_layout=True,)
        self.axis = self.fig.add_subplot(111)  # 2row 1column，top graph
        self.axis.set_xlabel('Pixel')
        self.axis.set_ylabel('Intensity')
        self.axis.set_ylim(0, 70000)
        self.axis.set_xlim((0,3700))
        self.axis.set_xticks(np.arange(0, 3700, 200))

        self.axis.grid(linestyle='--')
        xticks = range(0,3648,200)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.win)
        self.canvas.get_tk_widget().grid(column=0, row=8,padx=0,pady=0,ipadx=10,ipady=10,sticky='W')
        # 让窗口显示出来
        self.win.deiconify()
        #让图表动态显示

    def updatedrawing(self):
        self.axis.clear()
        self.axis.grid(linestyle='--')
        self.axis.set_ylim(0, 70000)
        self.axis.set_xlim((0, 3700))
        self.axis.set_xticks(np.arange(0, 3700, 200))
        i_range = arange(1,3648,1)-1
        yValues=self.result
        xValues = [i for i in range(0,len(yValues))]
        self.axis.plot(xValues, yValues, color='blue',linewidth=0.9)
        self.canvas.get_tk_widget().update()
        self.canvas.draw()
        sleep(0.1)

    #演示按钮
    def demobtnclicked(self):
        self.demoflag = not self.demoflag
        print(self.demoflag)
        while self.demoflag:
            self.updatedemodrawing()
            if not self.demoflag:
                break

    #演示数据刷新显示
    def updatedemodrawing(self):
        self.axis.clear()
        self.axis.grid(linestyle='--')
        self.axis.set_ylim(0, 70000)
        self.axis.set_xlim((0, 3700))
        self.axis.set_xticks(np.arange(0, 3700, 200))
        i_range = arange(1, 3648, 1) - 1
        yValues = self.pixeltool.getdemoresult()
        xValues = [i for i in range(0, len(yValues))]
        self.axis.plot(xValues, yValues, color='blue', linewidth=0.9)
        self.canvas.get_tk_widget().update()
        self.canvas.draw()
        sleep(0.1)


    #点击运行按钮进行的操作
    def pixel_sample(self):
        sample_cmd = [0x53, 0x7D, 0xFF]
        self.runflag = not(self.runflag)
        if self.runflag:
            self.run['text'] = '停止'
        else:
            self.run['text'] = '运行'
        while self.runflag:
            #发送采集指令
            self.SI.write(b'S')
            #等待一段时间后从串口读数据
            sleep(1.5)
            raw = self.SI.alwaysread()
            #原始数据切片
            r1 = raw[42:7317 * 2]
            self.result = [int(r1[i:i + 4], 16) for i in range(0, len(r1)) if i % 4 == 0]

            status = self.pixeltool.getstatusresult(raw)
            self.treetable.insert('', 0, values=('Glit', '0', '65535', '1000', '7319', '3648'))
            self.treetable.insert('', 0, values=status)
            # print(status)
            #重新绘制表格
            self.updatedrawing()

    def openuart(self):
        #获得串口号，波特率，检校位等参数
        num = self.uartnumbox.get()
        baudrate = self.baud.get()
        check = self.checkbitcombo.get()
        args = [num,baudrate,check[0]]
        print(args)
        #创建SerialInterface实例
        self.SI = serialInterface.SerialInterface(args)
        if not self.openflag:
            try:
                self.openflag = self.SI.open()
            except:
                pass
            self.openbtn['text'] = '关闭'
        else:
            try:
                self.openflag = self.SI.close()
            except:
                pass
            self.openbtn['text'] = '打开'

oop1 = mainUI()
oop1.win.mainloop()
