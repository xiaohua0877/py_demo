# -*- coding: utf-8 -*-
import re
from openpyxl import Workbook
from openpyxl import load_workbook


def test_code_str():
    wb = load_workbook('flash.xlsx')
    wb.guess_types = True
    ws = wb.active
    ws['A1'] = 42
    ws.append([1, 2, 3])
    line = "36          8        456          0       1024        816   startup_stm32f746xx.o\n"
    b = line.split()
    ws.append(b)
    print(b)
    wb.save("flash.xlsx")


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def test_code_write(b):
    wb = load_workbook('flash.xlsx')
    wb.guess_types = True
    ws = wb.active
    len1 = len(b) - 1
    count = 0
    list11 = b
    while True:
        count += 1
        if len1 < count:
            break
        # print(list11)
        new_number = []
        for n in b[count]:
            if is_number(n) is True:
                new_number.append(int(n))
            else:
                new_number.append(n)
        b[count] = new_number
        ws.append(b[count])
    # ws.append(b)
    print(b)
    wb.save("flash.xlsx")


def open_file_txt():
    # 第一种方法
    f = open("flash.map", "r")  # 设置文件对象
    src_line = f.readline()
    line = src_line[:-1]
    count = 1
    flag = 0
    res_list = []
    while src_line:  # 直到读取完文件
        src_line = f.readline()  # 读取一行文件，包括换行符
        count += 1
        line = src_line[:-1]
        if len(line) < 3 or line.endswith('------') or line.startswith('====='):
            continue
        # print('第%s行:%s' % (count, line))
        if 'Image component' in line:
            flag = 1
            continue
        if flag == 1:
            print('第%s行:%s' % (count, line))
            result = line.split()
            print(result)
            res_list.append(result)

    f.close()  # 关闭文件
    return res_list


# test_code_str()
b = open_file_txt()
test_code_write(b)

'''
#第二种方法
data = []
for line in open("data.txt","r"): #设置文件对象并读取每一行文件
    data.append(line)               #将每一行文件加入到list中


#第三种方法
f = open("data.txt","r")   #设置文件对象
data = f.readlines()  #直接将文件中按行读到list里，效果与方法2一样
f.close()             #关闭文件


print('第%s行:%s' % (count, line))
b = re.findall(r"\d+\.?\d*",line)
print(b)
pattern = re.compile(r'([a-z]*).o\n')
result = pattern.findall(line)
print(result)
'''
