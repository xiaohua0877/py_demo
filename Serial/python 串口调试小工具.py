import serial.tools.list_ports
import serial
from tkinter import Tk, StringVar, Label, Button, Listbox, Text, END
import time
import datetime
import re
import threading
import json

global serial_com
port_list = list(serial.tools.list_ports.comports())  # 读串口
print(port_list)
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


def thread_recv():  # 接收数据显示数据
    while True:
        for i in range(20):
            time_data = datetime.datetime.now()
            read = ser.readall()
            if len(read) > 0:
                hexShow(read, time_data)
                ##strShow(read, time_data)
            if on_hit == False:
                break
        if on_hit == False:
            break
        data_text1.delete(1.0, END)


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
    global value, serial_com
    value = lis.get(lis.curselection())
    var1.set(value)
    print(serial_com[lis.curselection()[0]])
    data1 = open("dump.txt", "r")
    data2 = json.load(data1)
    data1.close()
    data_text2.delete(1.0, END)
    data_text2.insert(1.0, data2)


on_hit = False


def open_serial():
    global on_hit, var3, ser, value
    # src = data_text2.get(1.0, END).strip().replace('\n', '').encode()
    #
    # src1 = bytes(src).decode('ascii')
    # print(src1)
    time.sleep(0.1)
    data = open("dump.txt", "w")
    # json.dump(src1, data)
    data.close()
    print(1)

    # ser = serial.Serial()
    # ser.baudrate = 9600  # 设置波特率（这里使用的是stc89c52）
    # ser.port = 'COM3'  # 端口是COM3
    # print(ser)
    # ser.open()  # 打开串口
    # print(ser.is_open)  # 检验串口是否打开
    if on_hit == False:
        print("port", value)
        # print(src1)

        ser = serial.Serial(  # 下面这些参数根据情况修改
            port=value,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            timeout=0.23,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        print("串口打开")

        var3.set('关闭串口')
        on_hit = True
        recv_data = threading.Thread(target=thread_recv)
        recv_data.start()
    else:
        on_hit = False
        ser.close()
        var3.set("打开串口")
        print("串口关闭")


def hexShow(argv, time_data):  # 接收数据格式调整
    # result = ''
    # hlen = len(argv)
    # for i in range(hlen):
    #     hvol = argv[i]
    #     hhex = hex(hvol)[2:]
    #     result += hhex.upper() + ' '
    # result = "%s: %s " % time_data + argv
    # data_text1.insert(1.0, result + '\n')
    result = ''
    hlen = len(argv)
    for i in range(hlen):
        hvol = argv[i]
        hhex = hex(hvol)[2:]
        result += hhex.upper() + ' '
    result = str(argv, encoding="utf-8")
    result = "%s:  " % time_data + result
    data_text1.insert(1.0, result + '\n')

def strShow(argv, time_data):  # 接收数据格式调整
    # result = ''
    # hlen = len(argv)
    # for i in range(hlen):
    #     hvol = argv[i]
    #     hhex = hex(hvol)[2:]
    #     result += hhex.upper() + ' '
    # result = "%s:" % time_data + result
    data_text1.insert(1.0, argv + '\n')

def get_data():  # 协议输入提取和转码
    global ser
    req1 = []
    src = data_text.get(1.0, END).strip().replace('\n', '').encode()

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
init_window.geometry("1000x250+10+10")
var1 = StringVar()

l = Label(init_window, bg='yellow', width=14, textvariable=var1)
l.grid(row=0, column=0)

var3 = StringVar()
var3.set('打开串口')
b1 = Button(init_window, text='串口', width=10, height=1, command=print_selection)
b1.grid(row=1, column=0)
b2 = Button(init_window, textvariable=var3, width=10, height=1, command=open_serial)
b2.grid(row=1, column=2)
b2 = Button(init_window, text="发送", width=10, height=1, command=get_data)
b2.grid(row=1, column=4)
b3 = Button(init_window, text="刷新串口", width=9, height=1, command=freshen)
b3.place(x=15, y=150)
t = Label(init_window, text="波特率")
t.grid(row=0, column=1)
var2 = StringVar()
var2.set(tuple(serial_com))
print("chuangk", serial_com)
value = 'COM3'
value = 'COM9'


lis = Listbox(init_window, width=10, height=5, listvariable=var2)  # 显示串口
lis.place(x=15, y=55)
data_text = Text(init_window, width=80, height=1)  # 输入传输字符
data_text.grid(row=1, column=3)
data_text1 = Text(init_window, width=90, height=100)  # 接收字符
data_text1.grid(row=2, column=3)
data_text2 = Text(init_window, width=10, height=1)  # 波特率设置
data_text2.grid(row=1, column=1)


data_text2.insert(END,'115200')

init_window.mainloop()
