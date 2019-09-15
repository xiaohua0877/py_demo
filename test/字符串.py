#!/usr/bin/python

str = "Line1-abcdef \nLine2-abc \nLine4-abcd"
print(str.split( ))
print(str.split(' ', 1 ))
import json
Prefer = {"jim": {"War": 1.9, "the big bang": 1.0, "The lord of wings": 4.0, "Beautiful America": 4.7}, "lily": {"War": 2.0, "Kongfu": 4.1, "The lord of wings": 3.6}, "tommy": {"War": 2.3, "Kongfu": 5.0, "The lord of wings": 3.0}, "jack": {"War": 2.8, "Kongfu": 5.5, "The lord of wings": 3.5}}
print('将字典一行显示不换行')
print(json.dumps(Prefer))
print('将字典按照json样式可视化显示')
print(json.dumps(Prefer,indent=4))


dic1 = {'type':'dic1','username':'loleina','age':16}
json_dic1 = json.dumps(dic1)
print(json_dic1)
# json_dic2 = json.dumps(dic1,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True )
# print(json_dic2)
