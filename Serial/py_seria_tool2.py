# -*- coding:utf-8 -*-
import serial.tools.list_ports
import serial
from tkinter import Tk, StringVar, IntVar, Label, Button, Listbox, Text, END, Radiobutton, Checkbutton
import time
import datetime
import re
import threading
import json

global serial_com, File_name
port_list = list(serial.tools.list_ports.comports())  # 读串口
# print(port_list)
print("port_list:{} ".format(port_list))
File_name = 'dump.json'

serial_com = []
if len(port_list) <= 0:
    print("The Serial port can't find!")

else:
    x = len(port_list)
    for i in range(x):
        port_list_0 = list(port_list[i])
        print(port_list_0[0])
        serial_com.append(port_list_0[0])
print(serial_com)


def show_rec_msg(read, time_data):
    tmp = rbtn_var.get()
    ##print(tmp)
    if tmp == 'output_hex':
        hexShow(read, time_data)
    else:
        strShow(read, time_data)


def thread_recv():  # 接收数据显示数据
    while True:
        for i in range(20):
            if (chbtn_val.get() == 1):
                time_data = datetime.datetime.now()
            else:
                time_data = ''
            read = ser.readall()
            if len(read) > 0:
                show_rec_msg(read, time_data)
            if on_hit == False:
                break
        if on_hit == False:
            break
        text_recv.delete(1.0, END)


def freshen():  # 刷新串口
    global serial_com
    lis.delete(END, )
    port_list = list(serial.tools.list_ports.comports())  # 读串口
    serial_com = []
    print(port_list)
    if len(port_list) <= 0:
        print("The Serial port can't find!")
    else:
        x = len(port_list)
        for i in range(x):
            port_list_0 = list(port_list[i])
            print(port_list_0[0])
            serial_com.append(port_list_0[0])
    print('端口', serial_com)
    var2.set(tuple(serial_com))


def print_selection():  # 选择串口
    global val_com, serial_com
    val_com = lis.get(lis.curselection())
    var1.set(val_com)
    text_baud.delete(1.0, END)
    text_baud.insert(1.0, data2)


# 第6步，定义选项触发函数功能
def print_btn_selection():
    rbtn_lab.config(text='' + rbtn_var.get())
    print('you have selected ' + rbtn_var.get())


def print_chbtn_selection():
    if (chbtn_val.get() == 1):
        print("input stampe")


on_hit = False

'''
ser = serial.Serial()
ser.baudrate = 9600  # 设置波特率（这里使用的是stc89c52）
ser.port = 'COM3'  # 端口是COM3
print(ser)
ser.open()  # 打开串口
print(ser.is_open)  # 检验串口是否打开
'''


def open_serial():
    global on_hit, open_btn_name, ser, val_com
    f = open(File_name, encoding='utf-8')
    content = f.read()  # 使用loads()方法，需要先读文件
    user_dic = json.loads(content)
    print(user_dic)
    print(type(user_dic))  # 打印res类型
    print(user_dic.keys())  # 打印字典的所有Key
    src1 = user_dic['com_info']['baudrate']
    val_com = user_dic['com_info']['port']
    print(src1)
    f.close()
    time.sleep(0.1)

    if on_hit == False:
        print("port", val_com)
        print(src1)
        ser = serial.Serial(  # 下面这些参数根据情况修改
            port=val_com,
            baudrate=src1,
            parity=serial.PARITY_NONE,
            timeout=0.23,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        print("串口打开")
        open_btn_name.set('关闭串口')
        on_hit = True
        recv_data = threading.Thread(target=thread_recv)
        recv_data.start()
    else:
        on_hit = False
        ser.close()
        open_btn_name.set("打开串口")
        print("串口关闭")


def hexShow(argv, time_data):  # 接收数据格式调整
    result = ''
    hlen = len(argv)
    for i in range(hlen):
        hvol = argv[i]
        hhex = hex(hvol)[2:]
        result += hhex.upper() + ' '
    result = "%s: " % time_data + result
    text_recv.insert(1.0, result + '\n')


def strShow(argv, time_data):  # 接收数据格式调整
    result = str(argv, encoding="utf-8")
    result = "%s:  " % time_data + result
    text_recv.insert(END, result + '\n')


def get_data():  # 协议输入提取和转码
    global ser
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
    ser.write(data)


init_window = Tk()

init_window.title('串口发送工具')
# 例如我们要设置窗口宽为100像素大小，高为50像素大小，形成一个长方形的窗口。即geometry("100x50")
# init_window.geometry("1000x600+10+10")
init_window.geometry("900x600")
var1 = StringVar()

l = Label(init_window, bg='yellow', width=14, textvariable=var1)
l.grid(row=0, column=0)

open_btn_name = StringVar()
open_btn_name.set('打开串口')
b2 = Button(init_window, textvariable=open_btn_name, width=10, height=1, command=open_serial)
b2.grid(row=1, column=0)

t = Label(init_window, text="波特率")
t.place(x=15, y=60)

text_baud = Text(init_window, width=10, height=1)  # 波特率设置
text_baud.place(x=15, y=60 + 30)
text_baud.insert(END, '115200')

b1 = Button(init_window, text='串口', width=10, height=1, command=print_selection)
b1.place(x=15, y=60 + 30 + 30)  # 60
# b1.grid(row=1, column=2)

var2 = StringVar()
var2.set(tuple(serial_com))
lis = Listbox(init_window, width=10, height=5, listvariable=var2)  # 显示串口
lis.place(x=15, y=160)  # 95
print("chuangk", serial_com)
val_com = 'COM9'

b3 = Button(init_window, text="刷新串口", width=9, height=1, command=freshen)
b3.place(x=15, y=160 + 100)  # 200

rbtn_lab = Label(init_window, bg='yellow', width=10, text='empty')
rbtn_lab.place(x=15, y=260 + 30)

rbtn_var = StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.
rbtn_var.set('output_str')  # # 如果1，那么儒家被默认选中
rbtn = Radiobutton(init_window, text='字符输出', variable=rbtn_var, value='output_str', command=print_btn_selection)
rbtn.place(x=15, y=290 + 30)
rbtn = Radiobutton(init_window, text='hex输出', variable=rbtn_var, value='output_hex', command=print_btn_selection)
rbtn.place(x=15, y=320 + 30)

chbtn_val = IntVar()  # 定义var1和var2整型变量用来存放选择行为返回值
chbtn_tim = Checkbutton(init_window, text='timestamp', variable=chbtn_val, onvalue=1, offvalue=0,
                        command=print_chbtn_selection)
chbtn_tim.place(x=15, y=350 + 30)

b2 = Button(init_window, text="发送", width=10, height=1, command=get_data)
b2.grid(row=1, column=4)
text_send = Text(init_window, width=80, height=1)  # 输入传输字符
text_send.grid(row=1, column=3)
text_recv = Text(init_window, width=90, height=100)  # 接收字符
text_recv.grid(row=2, column=3)

init_window.mainloop()
