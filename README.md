# py_demo



# bat批处理执行python 的几种方式  #
## 第三种方式: 用python打成包文件运行即可 ##
首先安装包： pip install pyinstaller    速度慢可以添加国内源 

安装成功后， 在当前的文件夹路径下  运行命令  pyinstaller  ***.py 文件 

接着会自动打包成一个可执行的 exe文件 ，点击这个可执行文件即可

# 第一种方式:#  
@echo off  
C:  
cd C:\Users\ldl\Desktop

start python test100.py 

start python 1.py 

start python 1.py 10

start python 1.py 100 

exit


## .bat 文件调用python脚本 ##
1.将clearlog.py 脚本放在指定目录 比如 我放在 C:\Users\Administrator\Desktop 上 也就是桌面上 

2.创建一个.bat 位后缀名的脚本

3.写入如下脚本

@echo off 

cd  C:\Users\Administrator\Desktop

start python clearlog.py


