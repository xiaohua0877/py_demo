import re
#第一种方法
f = open("flash.map","r")   #设置文件对象
line = f.readline()
line = line[:-1]
count=1
flag = 0
while line:             #直到读取完文件
    line = f.readline()  #读取一行文件，包括换行符
    #line = line[:-1]
    #print('第%s行:%s' % (count, line))
    if 'Image component' in line :
        flag = 1
    if flag == 1:
        print('第%s行:%s' % (count, line))
        b = re.findall(r"\d+\.?\d*",line)
        print(b)
        pattern = re.compile(r'([a-z]*).o\n')
        result = pattern.findall(line)
        print(result)
    count += 1
f.close() #关闭文件

'''
#第二种方法
data = []
for line in open("data.txt","r"): #设置文件对象并读取每一行文件
    data.append(line)               #将每一行文件加入到list中


#第三种方法
f = open("data.txt","r")   #设置文件对象
data = f.readlines()  #直接将文件中按行读到list里，效果与方法2一样
f.close()             #关闭文件
'''