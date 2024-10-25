# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 21:21:19 2024

@author: 92470
"""

#导入库
import struct
import sys
import binascii
import pdb
import os

#设置基础变量
startPy = 0x1540;
startChinese = 0x2628;
GPy_Table = {}

#定义函数
def byte2str(data):
    i = 0;
    length = len(data)
    ret = u''
    while i < length:
        x = data[i:i+2]
        t =  chr(struct.unpack('H', x)[0])
        if t == u'\r':
            ret += u'\n'
        elif t != u' ':
            ret += t
        i += 2
    return ret
def getPyTable(data):
    if data[0:4] != bytes(map(ord,"\x9D\x01\x00\x00")):
        return None
    data = data[4:]
    pos = 0
    length = len(data)
    while pos < length:
        index = struct.unpack('H', data[pos:pos +2])[0]
        pos += 2
        l = struct.unpack('H', data[pos:pos + 2])[0]
        pos += 2
        py = byte2str(data[pos:pos + l])
        GPy_Table[index] = py
        pos += l
def getWordPy(data):
    pos = 0
    length = len(data)
    ret = u''
    while pos < length:
        index = struct.unpack('H', data[pos:pos + 2])[0]
        ret += GPy_Table[index]
        pos += 2
    return ret
def getWord(data):
    pos = 0
    length = len(data)
    ret = u''
    while pos < length:
        index = struct.unpack('H', data[pos:pos +2])[0]
        ret += GPy_Table[index]
        pos += 2
    return ret
def getChinese(data):
    pos = 0
    length = len(data)
    while pos < length:
        same = struct.unpack('H', data[pos:pos + 2])[0]
        pos += 2
        py_table_len = struct.unpack('H', data[pos:pos + 2])[0]
        pos += 2
        py = getWordPy(data[pos: pos + py_table_len])
        pos += py_table_len
        for i in range(same):
            c_len = struct.unpack('H', data[pos:pos +2])[0]
            pos += 2
            word = byte2str(data[pos: pos + c_len])
            pos += c_len
            ext_len = struct.unpack('H', data[pos:pos +2])[0]
            pos += 2
            count = struct.unpack('H', data[pos:pos +2])[0]
            GTable.append((count, py, word))
            pos += ext_len
def deal(file_name):
    print('-' * 60)
    f = open(file_name, 'rb')
    data = f.read()
    f.close()
    if data[0:12] != bytes(map(ord,"\x40\x15\x00\x00\x44\x43\x53\x01\x01\x00\x00\x00")):
        pass
    getPyTable(data[startPy:startChinese])
    getChinese(data[startChinese:])
def txt_dict(txt):
    txts = txt.copy()
    for i in range(len(txt)):
        tr = txt[0][i]
        m = re.search(r' ',tr)
        txts[0][i]=tr[m.start()+1:]
    return txts

# 细胞词库scel文件所在路径
path=r'D:\\dictionary'
os.chdir(path)
files=os.listdir(path)

# 对所有文件进行循环
for i in range(len(files)):
    try:
        GTable=[]
        o=[files[i]]
        for f in o:
            deal(f)
            # 定义转化后的txt文档所在路径
            with open (f'D:\\dictionary\\{files[i][:-5]}.txt','w',encoding='utf8') as f:
                for word in GTable:
                    f.write(word[2]+'\n')
        print(f"第{i}个文件已转化")
    except:
        print(f'{i}个文件有问题')
        continue
    