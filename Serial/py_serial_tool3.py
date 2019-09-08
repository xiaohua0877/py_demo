# -*- coding:utf-8 -*-
import serial.tools.list_ports
import serial
import tkinter
from tkinter import Tk, StringVar, IntVar, Label, Button, Listbox, Text, END, Radiobutton, Checkbutton
import time
import datetime
import re
import threading
import json


class MyDevice():
    def __init__(self):
        self.serial_com = ''
        self.on_hit = False
        self.val_com = ''
        self.open_btn_name = ''
        self.ser = ''
        """Initialize attributes to describe a car."""
        port_list = list(serial.tools.list_ports.comports())  # 读串口
        # print(port_list)
        print("port_list:{} ".format(port_list))
        self.File_name = 'dump.json'

        self.serial_com = []
        if len(port_list) <= 0:
            print("The Serial port can't find!")

        else:
            x = len(port_list)
            for i in range(x):
                port_list_0 = list(port_list[i])
                print(port_list_0[0])
                self.serial_com.append(port_list_0[0])
        print(self.serial_com)

    def show_rec_msg(self, read, time_data):
        tmp = self.rbtn_var.get()
        ##print(tmp)
        if tmp == 'output_hex':
            self.hexShow(read, time_data)
        else:
            self.strShow(read, time_data)

    def thread_recv(self):  # 接收数据显示数据
        step=0
        while True:
            step +=1
            if (self.chbtn_val.get() == 1):
                time_data = datetime.datetime.now()
            else:
                time_data = ''
            read = self.ser.readall()
            if len(read) > 0:
                self.show_rec_msg(read, time_data)
            if self.on_hit == False:
                break
            if(step > 20):
                self.text_recv.delete(1.0, 2.0)
        # if self.on_hit == False:
        #     break

    def freshen(self):  # 刷新串口
        self.com_list.delete(END, )
        port_list = list(serial.tools.list_ports.comports())  # 读串口
        self.serial_com = []
        print(port_list)
        if len(port_list) <= 0:
            print("The Serial port can't find!")
        else:
            x = len(port_list)
            for i in range(x):
                port_list_0 = list(port_list[i])
                print(port_list_0[0])
                self.serial_com.append(port_list_0[0])
        print('端口', self.serial_com)
        self.com_list_val.set(tuple(self.serial_com))


    def print_selection(self):  # 选择串口
        self.val_com = self.com_list.get(self.com_list.curselection())
        self.com_select_var.set(self.val_com)
        # text_baud.delete(1.0, END)
        # text_baud.insert(1.0, data2)


    # 第6步，定义选项触发函数功能
    def print_btn_selection(self):
        self.rbtn_lab.config(text='' + self.rbtn_var.get())
        print('you have selected ' + self.rbtn_var.get())


    def print_chbtn_selection():
        if (self.chbtn_val.get() == 1):
            print("input stamp")


    def open_serial(self):
        # global    val_com
        f = open(self.File_name, encoding='utf-8')
        content = f.read()  # 使用loads()方法，需要先读文件
        user_dic = json.loads(content)
        print(user_dic)
        print(type(user_dic))  # 打印res类型
        print(user_dic.keys())  # 打印字典的所有Key
        src1 = user_dic['com_info']['baudrate']
        self.val_com = user_dic['com_info']['port']
        print(src1)
        f.close()
        time.sleep(0.1)

        if self.on_hit == False:
            print("port", self.val_com)
            print(src1)
            self.ser = serial.Serial(  # 下面这些参数根据情况修改
                port=self.val_com,
                baudrate=src1,
                parity=serial.PARITY_NONE,
                timeout=0.23,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS)
            print("串口打开")
            self.open_btn_name.set('关闭串口')
            self.on_hit = True
            recv_data = threading.Thread(target=self.thread_recv)
            recv_data.start()
        else:
            self.on_hit = False
            self.ser.close()
            self.open_btn_name.set("打开串口")
            print("串口关闭")


    def hexShow(self, argv, time_data):  # 接收数据格式调整
        result = ''
        hlen = len(argv)
        for i in range(hlen):
            hvol = argv[i]
            hhex = hex(hvol)[2:]
            result += hhex.upper() + ' '
        result = "%s: " % time_data + result
        self.text_recv.insert(1.0, result + '\n')


    def strShow(self, argv, time_data):  # 接收数据格式调整
        result = str(argv, encoding="utf-8")
        result = "%s:  " % time_data + result
        self.text_recv.insert(END, result + '\n')


    def get_data(self):  # 协议输入提取和转码
        req1 = []
        src = text_send.get(1.0, END).strip().replace('\n', '').encode()
        print(len(src))
        print(src)
        req = re.findall(r"[^' ']", src.decode())
        print(req)
        j = 0
        while True:
            try:
                data = req[j] + req[j + 1]
                req1.append(data)
                if j + 1 < len(req):
                    j += 2
            except IndexError:
                break
        print(req1)
        st = []
        for i in range(len(req1)):
            a = int(req1[i], 16)
            print(a)
            st.append(a)
        print(st)
        a = str(len(st)) + 'B'
        data = bytes(st)
        self.ser.write(data)


    def init_wim(self):
        init_window = Tk()

        init_window.title('串口发送工具')
        # 例如我们要设置窗口宽为100像素大小，高为50像素大小，形成一个长方形的窗口。
        # init_window.geometry("1000x600+10+10")
        init_window.geometry("900x600")
        self.com_select_var = StringVar()

        l = Label(init_window, bg='yellow', width=14, textvariable=self.com_select_var)
        l.grid(row=0, column=0)

        self.open_btn_name = StringVar()
        self.open_btn_name.set('打开串口')
        b2 = Button(init_window, textvariable=self.open_btn_name, width=10, height=1, command=self.open_serial)
        b2.grid(row=1, column=0)

        t = Label(init_window, text="波特率")
        t.place(x=15, y=60)

        text_baud = Text(init_window, width=10, height=1)  # 波特率设置
        text_baud.place(x=15, y=60 + 30)
        text_baud.insert(END, '115200')

        b1 = Button(init_window, text='串口', width=10, height=1, command=self.print_selection)
        b1.place(x = 15, y = 90 + 30)  # 60
 
        self.com_list_val = StringVar()
        self.com_list_val.set(tuple(self.serial_com))
        self.com_list = Listbox(init_window, width=10, height=3, listvariable=self.com_list_val)  # 显示串口
        self.com_list.place(x=15, y=160)  # 95
        print("serial_com", self.serial_com)
        self.val_com = self.serial_com[0]
        #self.val_com = 'COM9'




        b3 = Button(init_window, text="刷新串口", width=9, height=1, command=self.freshen)
        b3.place(x=15, y=160 + 100)  # 200

        self.rbtn_lab = Label(init_window, bg='yellow', width=10, text='empty')
        self.rbtn_lab.place(x=15, y=260 + 30)

        self.rbtn_var = StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.
        self.rbtn_var.set('output_str')  # # 如果1，那么儒家被默认选中
 
        rbtn = Checkbutton(init_window, text='hex接收', variable=self.rbtn_var, onvalue='output_hex',
                           offvalue='output_str', command=self.print_btn_selection)
        rbtn.place(x=15, y=320 + 30)

        self.chbtn_val = IntVar()  # 定义var1和var2整型变量用来存放选择行为返回值
        chbtn_tim = Checkbutton(init_window, text='timestamp', variable=self.chbtn_val, onvalue=1, offvalue=0,
                                command=self.print_chbtn_selection)
        chbtn_tim.place(x=15, y=350 + 30)

        b2 = Button(init_window, text="发送", width=10, height=1, command=self.get_data)
        b2.grid(row=1, column=4)
        text_send = Text(init_window, width=80, height=1)  # 输入传输字符
        text_send.grid(row=1, column=3)
        self.text_recv = Text(init_window, width=90, height=90)  # 接收字符
        self.text_recv.grid(row=2, column=3)
        init_window.mainloop()


my_serial = MyDevice()
my_serial.init_wim()



'''
            while True:
                for i in range(20):
                    if (self.chbtn_val.get() == 1):
                        time_data = datetime.datetime.now()
                    else:
                        time_data = ''
                    read = self.ser.readall()
                    if len(read) > 0:
                        self.show_rec_msg(read, time_data)
                    if self.on_hit == False:
                        break
                if self.on_hit == False:
                    break
                self.text_recv.delete(1.0, END)
'''