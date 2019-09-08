import serial.tools.list_ports
import serial
from tkinter import Tk, StringVar, Label, Button, Listbox, Text, END
import time
import datetime
import re
import threading
import json

global serial_com,File_name
port_list = list(serial.tools.list_ports.comports())  # 读串口
#print(port_list)
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
    strShow(read, time_data)

def thread_recv():  # 接收数据显示数据
    while True:
        for i in range(20):
            time_data = datetime.datetime.now()
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
    print(serial_com[lis.curselection()[0]])
    data1 = open(File_name, "r")
    data2 = json.load(data1)
    data1.close()
    text_baud.delete(1.0, END)
    text_baud.insert(1.0, data2)


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
    result = "%s: %s " % time_data + argv
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
init_window.geometry("1000x250+10+10")
var1 = StringVar()

l = Label(init_window, bg='yellow', width=14, textvariable=var1)
l.grid(row=0, column=0)

open_btn_name = StringVar()
open_btn_name.set('打开串口')
b1 = Button(init_window, text='串口', width=10, height=1, command=print_selection)
b1.grid(row=1, column=0)
b2 = Button(init_window, textvariable=open_btn_name, width=10, height=1, command=open_serial)
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
#val_com = 'COM3'
val_com = 'COM9'

lis = Listbox(init_window, width=10, height=5, listvariable=var2)  # 显示串口
lis.place(x=15, y=55)
text_send = Text(init_window, width=80, height=1)  # 输入传输字符
text_send.grid(row=1, column=3)
text_recv = Text(init_window, width=90, height=100)  # 接收字符
text_recv.grid(row=2, column=3)
text_baud = Text(init_window, width=10, height=1)  # 波特率设置
text_baud.grid(row=1, column=1)
text_baud.insert(END, '115200')

init_window.mainloop()
