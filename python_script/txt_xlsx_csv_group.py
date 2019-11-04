# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import warnings
import winreg
warnings.filterwarnings("ignore")    #忽略警告
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
ospath = winreg.QueryValueEx(key, "Desktop")[0]    #读取Windows电脑桌面路径

d1 = pd.read_table(ospath + '\\file\\file1.txt',header=None)   #读取要处理的文件
d2 = pd.read_table(ospath + '\\file\\file2.csv',header=None)
d3 = pd.read_excel(ospath + '\\file\\file3.xlsx',header=None)

d1.columns = ['时间','业务','渠道/总计','渠道号','注册用户','登录用户','付费用户','付费转化率','复充用户','复充率','付费新用户','付费新用户占比','总抽取价值','折现价值','折现率','充值收入','提现价值','背包价值','返奖率']
d1['渠道号'] = d1['渠道号'].fillna(90000)    #处理空值
d1['渠道号'] = d1['渠道号'].astype(int)    #转换字段的格式

d4 = pd.concat([d2,d3],axis=0)    #数据拼接，将不同地方的数据拼接到一起
d4.columns = ['时间','业务','渠道/总计','渠道号','UV']
d4['渠道号'] = d4['渠道号'].fillna(90000)
d5 = d4
m1 = d5.groupby(['时间','业务','渠道/总计','渠道号'])['UV'].sum().reset_index()    #数据聚合
m = m1.drop(m1[(m1.渠道号=='None')].index.tolist())

m['渠道号'] = m['渠道号'].astype(int)
n = pd.merge(m,d1,how='inner',on=['时间','业务','渠道/总计','渠道号'])    #数据聚合

def func(x,y):
    if x == 0:
        z = 0
    else:
        z = y/x
    return z

n['UV价值'] = n.apply(lambda x:func(x.UV,x.充值收入),axis=1)    #补充计算字段
n['注册转化率'] = n.apply(lambda x:func(x.UV,x.注册用户),axis=1)
n['登录转化率'] = n.apply(lambda x:func(x.UV,x.登录用户),axis=1)
n['ARPU值'] = n.apply(lambda x:func(x.付费用户,x.充值收入),axis=1)

cols = list(n)    #调整各列的位置
cols.insert(5,cols.pop(cols.index('UV价值')))
cols.insert(7,cols.pop(cols.index('注册转化率')))
cols.insert(9,cols.pop(cols.index('登录转化率')))
cols.insert(14,cols.pop(cols.index('ARPU值')))
data = n.loc[:,cols]
data.to_excel(ospath + '\\file\\result.xlsx',index = False)