# -*- coding: utf-8 -*-
import pandas as pd
import datetime

reg = pd.read_table(r'path\reg.txt')
pay = pd.read_table(r'path\pay.txt')

days1 = reg['create_time']    #读取注册信息
pids1 = reg['ID']
usrs = reg['reg_num']

days2 = pay['create_time']    #读取付费信息
pids2 = pay['ID']
interval_days = pay['interval_days']
pays = pay['pay_num']

def ltv_k(k):
    l = []
    for day1,pid1,usr in zip(days1,pids1,usrs):
        if k <= (datetime.datetime.strptime(str(max(days2)),'%Y%m%d').date() - datetime.datetime.strptime(str(day1),'%Y%m%d').date()).days:
            paylist = []
            for day2,pid2,interval_day,p in zip(days2,pids2,interval_days,pays):
                if day1 == day2 and pid1 == pid2 and interval_day <= k:
                    paylist.append(p)
            s = [sum(paylist)/usr]
        else:
            s = ['']
        l.append(s)
    dt = pd.DataFrame(l)
    ltvk = 'LTV'+str(k)
    n_dt = dt.rename(columns={0:ltvk})
    return n_dt

data = pd.concat([reg,ltv_k(1),ltv_k(2),ltv_k(3),ltv_k(4),ltv_k(5),ltv_k(6),ltv_k(7),ltv_k(8),ltv_k(9),ltv_k(10),ltv_k(11),ltv_k(12),ltv_k(13),ltv_k(14),ltv_k(15),ltv_k(16),ltv_k(17),ltv_k(18),ltv_k(19),ltv_k(20),ltv_k(21),
                 ltv_k(22),ltv_k(23),ltv_k(24),ltv_k(25),ltv_k(26)],axis = 1)


data.to_excel('path\\LTV.xlsx',index = False)
print('success!')