# #--web端比分直播--#
import re
from selenium import webdriver
import time
import requests
from lxml import etree
from itertools import zip_longest  #列表等分函数
web = webdriver.PhantomJS()
url = 'http://m.win007.com/'
web.get(url)
time.sleep(1)  #等待数据加载完毕

#手机web端请求头
headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',}

#PC网站请求头
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}

def get_data_list():   #获得即时赛事所在的区域，该区域为表格
    data_list = web.find_elements_by_xpath('//*[@style="display:block"]')
    return data_list

def get_jishi():  #获取全部的即时数据
    for data in get_data_list():
        data = data.text.split('\n') #已分割，后续便于处理
        print(data) #列表输出

def get_zucai():   #足彩
    web.find_elements_by_xpath('//*[@id="logolink"]/a[1]/img')[0].click()
    time.sleep(1)
    web.find_elements_by_xpath('//*[@id="menu"]/li[3]')[0].click()
    time.sleep(1)
    table_list = web.find_elements_by_xpath('//*[@style="display:block"]')
    for table in table_list:
        table = table.text.split('\n')
        print(table)
        
def get_jingcai():   #竞彩
    web.find_elements_by_xpath('//*[@id="logolink"]/a[1]/img')[0].click()
    time.sleep(1)
    web.find_elements_by_xpath('//*[@id="menu"]/li[4]')[0].click()
    time.sleep(1)
    table_list = web.find_elements_by_xpath('//*[@style="display:block"]')
    for table in table_list:
        table = table.text.split('\n')
        print(table)
        
def get_danchang():   #单场
    web.find_elements_by_xpath('//*[@id="logolink"]/a[1]/img')[0].click()
    time.sleep(1)
    web.find_elements_by_xpath('//*[@id="menu"]/li[5]')[0].click()
    time.sleep(1)
    table_list = web.find_elements_by_xpath('//*[@style="display:block"]')
    for table in table_list:
        table = table.text.split('\n')
        print(table)          
        
        
def get_matchids():  #获取比赛id
    matchids = []
    for data in get_data_list():
        matchids.append(data.get_attribute('id').lstrip('match_'))  #获取赛事ID
    return matchids


def get_team_rank():   #球队排名信息
    for matchid in get_matchids():
        try:
            url = 'http://zq.win007.com/analysis/{}cn.htm'.format(str(matchid))
            time.sleep(2)
            html = requests.get(url,headers = header)
            html.encoding = 'utf-8'
            html = html.text
            team = re.compile('<td height=28 colspan=11.*?><b>(.*?)</b></font></a></td>',re.S).findall(html)
            home_team = team[0]  #主队排名及主队名
            away_team = team[1]  #客队排名及客队名
            match_team = home_team + 'VS' + away_team   #输出示例
            print(match_team)
        except:
            print('数据缺失！')


#==============================R18 直播页面==================================#
#赛事事件的具体名称以输出为准，赛事不同，该区域展示的信息也不同，赛事信息的展示结构不统一

def shijian_zhibo():    #事件直播
    for matchid in get_matchids():
        try:
            url = 'http://m.win007.com/Analy/ShiJian/{}.htm'.format(str(matchid))   #循环抓取
            html = requests.get(url,headers = headers).text
            selector = etree.HTML(html)
            titles = re.compile('<div class="up"></div>(.*?)</div>',re.S).findall(html)
            title_list = []
            for item in titles:
                title_list.append(item.replace('\r\n','').strip())
            for i in range(0,len(title_list)):
                title = title_list[i]
                if title == '比赛事件':   #比赛事件需要单独处理
                    print(title)
                    print(url)
                    tables = selector.xpath('//*[@id="content"]/table')
                    trs = tables[i].xpath('tr')
                    for tr in trs:
                        res = tr.xpath('string(.)').split('\n')
                        dtlist = []
                        for item in res:
                            dtlist.append(item.strip().strip('\r').replace('\xa0',''))
                        for s in dtlist:
                            if s == '\r':
                                dtlist.remove(s)
                            while '' in dtlist:
                                dtlist.remove('')
                        pngs = tr.xpath('td/img/@src')
                        if len(pngs) > 0:
                            png = tr.xpath('td/img/@src')[0].split('/')[-1].split('@')[0]   #分割图片链接，接下来判断所属类别
                            if png == 'jinqiu':
                                dtlist.append('进球')
                            if png == 'dianqiu':
                                dtlist.append('点球')
                            if png == 'wulong':
                                dtlist.append('乌龙')
                            if png == '4':
                                dtlist.append('两黄变红')
                            if png == 'r_hu.png':
                                dtlist.append('换人')
                            if png == 'ycard':
                                dtlist.append('黄牌')
                            if png == 'rcard':
                                dtlist.append('红牌')
                            print(dtlist)
                            #jinqiu #进球、#dianqiu #点球、#wulong 乌龙、 #4 两黄变红、#r_hu  换人、#ycard 黄牌、#rcard 红牌                      
                else:
                    print(title)
                    print(url)    #检验用
                    tables = selector.xpath('//*[@id="content"]/table')
                    trs = tables[i].xpath('tr')
                    for tr in trs:
                        res = tr.xpath('string(.)').split('\n')
                        dtlist = []
                        for item in res:
                            dtlist.append(item.strip().strip('\r').replace('\xa0',''))
                        for s in dtlist:
                            if s == '\r':
                                dtlist.remove(s)
                            while '' in dtlist:
                                dtlist.remove('')
                        print(dtlist)
        except:
            print('数据缺失！')


#==============================R19 概率=================================#

def get_urls():
    urls = []
    for matchid in get_matchids():
        url = 'http://m.win007.com/analy/oddscomp/{}.htm'.format(str(matchid))
        urls.append(url)
    return urls

def get_oupei():  #近10场欧赔汇总数据
    for url in get_urls():
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        try:
            title = selector.xpath('//*[@id="content"]/div[2]')[0] 
            res = title.xpath('string(.)').split('\n')
            dtlist = []  #去除多余标签和空格，传入列表
            for item in res:  
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')  #去除列表中的空元素
            print(dtlist)
        except:
            print('数据缺失！')
            
def get_oupei_xq():  #获得对应10场赛事详情
    for url in get_urls():
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        try:
            tables = selector.xpath('//*[@id="content"]/table')
            res = tables[0].xpath('string(.)').split('\n')
            dtlist = []  #去除多余标签和空格，传入列表
            for item in res:  
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')  #去除列表中的空元素
            trs = dtlist[5:]
            from itertools import zip_longest  #列表等分函数
            n_groups = lambda seq, n:zip_longest(*[iter(seq)]*n)
            tr = list(n_groups(trs, 14))
            print(tr)  #输出列表，具体赛事信息为元组
        except:
            print('数据缺失！')
            
def get_yapei():  #近10场亚赔汇总
    for url in get_urls():
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        try:
            title = selector.xpath('//*[@id="content"]/div[3]')[0] 
            res = title.xpath('string(.)').split('\n')
            dtlist = []  #去除多余标签和空格，传入列表
            for item in res:  
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')  #去除列表中的空元素
            print(dtlist)
        except:
            print('数据缺失！')
            
def get_yapei_xq():  #获得对应10场赛事详情
    for url in get_urls():
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        try:
            tables = selector.xpath('//*[@id="content"]/table')
            res = tables[1].xpath('string(.)').split('\n')
            dtlist = []  #去除多余标签和空格，传入列表
            for item in res:  
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')  #去除列表中的空元素
            trs = dtlist[5:]
            n_groups = lambda seq, n:zip_longest(*[iter(seq)]*n)
            tr = list(n_groups(trs, 14))
            print(tr)  #输出列表，具体赛事信息为元组
        except:
            print('数据缺失！')
            
def get_daxiao():  #近10场大小汇总
    for url in get_urls():
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        try:
            title = selector.xpath('//*[@id="content"]/div[4]')[0] 
            res = title.xpath('string(.)').split('\n')  #取xpath表达式定位的所有文本
            dtlist = []  #去除多余标签和空格，传入列表
            for item in res:  
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')  #去除列表中的空元素
            print(dtlist)
        except:
            print('数据缺失！')
            
def get_daxiao_xq():   #获得对应10场赛事详情
    for url in get_urls():
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        try:
            tables = selector.xpath('//*[@id="content"]/table')
            res = tables[2].xpath('string(.)').split('\n')
            dtlist = []  #去除多余标签和空格，传入列表
            for item in res:  
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')  #去除列表中的空元素
            trs = dtlist[5:]
            n_groups = lambda seq, n:zip_longest(*[iter(seq)]*n)   #列表等分，以14为步长等分列表，得到列表嵌套元组
            tr = list(n_groups(trs, 14))
            print(tr)  #输出列表，具体赛事信息为元组
        except:
            print('数据缺失！')
            
#===================================R20 分析  第一个版本暂不需要===================================#
def get_analyurl():   #拼接分析页面的链接
    urls = []
    for matchid in get_matchids():
        url = 'http://m.win007.com/analy/Analysis/{}.htm'.format(str(matchid))
        urls.append(url)
    return urls

def get_hometeam_score():  #主队积分
    for url in get_analyurl():
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        try:
            tables = selector.xpath('//*[@id="content"]/table')
            res = tables[0].xpath('string(.)').split('\n')
            dtlist = []
            for item in res:
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')
            trs = dtlist
            n_groups = lambda seq, n:zip_longest(*[iter(seq)]*n)
            score = list(n_groups(trs, 11))
            print(score)
        except:
            print('数据缺失！')
            
def get_awayteam_score():  #客队积分
    for url in get_analyurl():
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        try:
            tables = selector.xpath('//*[@id="content"]/table')
            res = tables[1].xpath('string(.)').split('\n')
            dtlist = []
            for item in res:
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')
            trs = dtlist
            n_groups = lambda seq, n:zip_longest(*[iter(seq)]*n)
            score = list(n_groups(trs, 11))
            print(score)
            print(url)
        except:
            print('数据缺失！')
        
#=============================================R21 赔率===============================================
#包含赔率历史记录，输出结果为列表，增加了异常处理和sleep,无数据的url打印‘数据缺失！’，暂未使用代理ip

def get_pei_keys():  #获得网址的KEY
    links = []
    for matchid in get_matchids():
        link = '{matchid}.htm'.format(matchid = str(matchid))
        links.append(link)
    return links


def get_match_time(html):   #获取开赛时间
    time = re.compile('rowspan="2">(.*?)&nbsp').findall(html)
    return time

#亚赔部分
def get_yapei_peilv():
    for matchid in get_matchids():
        url = 'http://m.win007.com/asian/{}.htm'.format(str(matchid))
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        trs = selector.xpath('//*[@id="hTable"]/tr')  #定位表格里所有的行
        for tr in trs:
            data = tr.xpath('string(.)').split('\n')  #抽取每行所有的文本信息并分割成列表
            dtlist = []
            for item in data:
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')
            print(dtlist)
    
def get_yapei_cids():  #获取不同公司的cid
    for matchid in get_matchids():
        url = 'http://m.win007.com/asian/{}.htm'.format(str(matchid))
        html = requests.get(url,headers = headers).text
        cids = re.compile('onclick="showDetail\(.*?,\'(.*?)\'\)">').findall(html)
        return cids
                
def get_yapei_change(): 
    #拼接赔率变化记录的网址,获得赔率变化记录   
    for cid in get_yapei_cids():
        for link in get_pei_keys():
            url = 'http://m.win007.com/asiandetail/' + str(cid) + '/' + str(link)
            time.sleep(2)
            if len(url) > 5:
                print(url)
                try:
                    html = requests.get(url,headers = headers).text
                    matchtime = get_match_time(html)[0]
                    mtime = datetime.strptime(matchtime,'%m-%d %H:%M')
                    spl = url.split('/')
                    pat = spl[-2] + '/' + spl[-1] + '.*?>(.*?)</a>'    #分割网址得到匹配公司名字的正则
                    company = re.compile(pat).findall(html)[0].strip()   #赔率公司
                    selector = etree.HTML(html)
                    trs = selector.xpath('//*[@id="hTable"]/tr')  #定位表格里所有的行
                    for tr in trs:
                        data = tr.xpath('string(.)').split('\n')
                        dtlist = []
                        for item in data:
                            dtlist.append(item.strip().strip('\r'))
                        for s in dtlist:
                            if s == '\r':
                                dtlist.remove(s)
                            while '' in dtlist:
                                dtlist.remove('')
                        dtlist = dtlist
                        ndtlist = dtlist[:-1]  #去除原列表里的日期和时间
                        beforetime = dtlist[-1]  #拼接日期和时间
                        btime = datetime.strptime(beforetime,'%m-%d %H:%M')  #字符串转换为时间
                        res_time = (mtime - btime).seconds/60 #计算相差分钟数
                        str_time = str(res_time)  #时间转换为字符串
                        ndtlist.append(str_time)  #将时间差添加到列表里
                        print(ndtlist)  #新的数据列表
                    print(company)
                except:
                    print('数据缺失！')                    
            
#欧赔部分
def get_oupei_peilv():
    for matchid in get_matchids():
        url = 'http://m.win007.com/compensate/{}.htm'.format(str(matchid))   #不在源码里，模拟浏览器
        web.get(url)
        time.sleep(1)
        trs = web.find_elements_by_xpath('//*[@id="hTable"]/tbody/tr')  #定位表格里所有的行
        for tr in trs:
            data = tr.text.split('\n')  #抽取每行所有的文本信息并分割成列表
            print(data)
        
def get_oupei_cids():  #获取不同公司的cid
    for matchid in get_matchids():
        url = 'http://m.win007.com/compensate/{}.htm'.format(str(matchid))
        html = requests.get(url,headers = headers).text
        cids = re.compile('"cId":(.*?),"hw"').findall(html)
        return cids

def get_oupei_change():  #获得赔率变化网址 #获得欧赔变化记录
    for cid in get_oupei_cids():
        for link in get_pei_keys():
            try:
                url = 'http://m.win007.com/CompensateDetail/' + str(cid) + '/' + str(link)
                html = requests.get(url,headers = headers).text
                matchtime = get_match_time(html)[0]
                mtime = datetime.strptime(matchtime,'%m-%d %H:%M')
                time.sleep(2)
                selector = etree.HTML(html)
                trs = selector.xpath('//*[@id="content"]/table[2]/tr')  #定位表格里所有的行
                for tr in trs:
                    data = tr.xpath('string(.)').split('\n')
                    dtlist = []
                    for item in data:
                        dtlist.append(item.strip().strip('\r'))
                    for s in dtlist:
                        if s == '\r':
                            dtlist.remove(s)
                        while '' in dtlist:
                            dtlist.remove('')
                    dtlist = dtlist
                    ndtlist = dtlist[:-2]  #去除原列表里的日期和时间
                    if len(dtlist) > 3:
                        beforetime = dtlist[-2] + ' '+ dtlist[-1]  #拼接日期和时间
                        btime = datetime.strptime(beforetime,'%m-%d %H:%M')  #字符串转换为时间
                        res_time = (mtime - btime).seconds/60 #计算相差分钟数
                        str_time = str(res_time)  #时间转换为字符串
                        ndtlist.append(str_time)  #将时间差添加到列表里
                        print(ndtlist)
                    else:
                        print(dtlist) #为了输出赔率变化记录所属的公司
            except:
                print('数据缺失！')

#大小部分
def get_daxiao_peilv():
    for matchid in get_matchids():
        url = 'http://m.win007.com/overunder/{}.htm'.format(str(matchid))
        html = requests.get(url,headers = headers).text
        selector = etree.HTML(html)
        trs = selector.xpath('//*[@id="oTable"]/tr')  #定位表格里所有的行
        for tr in trs:
            data = tr.xpath('string(.)').split('\n')  #抽取每行所有的文本信息并分割成列表
            dtlist = []
            for item in data:
                dtlist.append(item.strip().strip('\r'))
            for s in dtlist:
                if s == '\r':
                    dtlist.remove(s)
                while '' in dtlist:
                    dtlist.remove('')
            print(dtlist)
        
def get_daxiao_cids():  #获取不同公司的cid
    for matchid in get_matchids():
        url = 'http://m.win007.com/overunder/{}.htm'.format(str(matchid))
        html = requests.get(url,headers = headers).text
        cids = re.compile('onclick="showDetail\(.*?,\'(.*?)\'\)">').findall(html)
        return cids

def get_daxiao_change():
    #拼接赔率变化记录的网址 #获得赔率变化记录
    for cid in get_daxiao_cids():
        for link in get_pei_keys():
            try:
                url = 'http://m.win007.com/oudetail/' + str(cid) + '/' + str(link)
                time.sleep(2)
                html = requests.get(url,headers = headers).text
                matchtime = get_match_time(html)[0]
                mtime = datetime.strptime(matchtime,'%m-%d %H:%M')
                spl = url.split('/')
                pat = spl[-2] + '/' + spl[-1] + '.*?>(.*?)</a>'
                company = re.compile(pat).findall(html)[0].strip()   #赔率公司
                selector = etree.HTML(html)
                trs = selector.xpath('//*[@id="hTable"]/tr')  #定位表格里所有的行
                for tr in trs:
                    data = tr.xpath('string(.)').split('\n')
                    dtlist = []
                    for item in data:
                        dtlist.append(item.strip().strip('\r'))
                    for s in dtlist:
                        if s == '\r':
                            dtlist.remove(s)
                        while '' in dtlist:
                            dtlist.remove('')
                    dtlist = dtlist
                    ndtlist = dtlist[:-1]  #去除原列表里的日期和时间
                    beforetime = dtlist[-1]  #拼接日期和时间
                    btime = datetime.strptime(beforetime,'%m-%d %H:%M')  #字符串转换为时间
                    res_time = (mtime - btime).seconds/60 #计算相差分钟数
                    str_time = str(res_time)  #时间转换为字符串
                    ndtlist.append(str_time)  #将时间差添加到列表里
                    print(ndtlist)  #新的数据列表
                print(company)
            except:
                print('数据缺失！')

                
def bifa_zhishu():   #必发指数
    for matchid in get_matchids():
        try:
            url = 'http://vip.win007.com/betfa/single.aspx?id={}'.format(str(matchid))
            time.sleep(1)
            html = requests.get(url).text
            selector = etree.HTML(html)
            tr = selector.xpath('//*[@id="dataList"]/table/tr')
            home_res = tr[2].xpath('string(.)').split('\n')
            draw_res = tr[3].xpath('string(.)').split('\n')
            away_res = tr[4].xpath('string(.)').split('\n')
            #选项、成交价、成交量、比例、盈亏、冷热
            home = home_res[1].strip('\r') +  home_res[5].strip('\r') + home_res[8].strip('\r') + home_res[9].strip('\r') + home_res[12].strip('\r') + home_res[13].strip('\r')
            draw = draw_res[1].strip('\r') +  draw_res[4].strip('\r') + draw_res[6].strip('\r') + draw_res[7].strip('\r') + draw_res[10].strip('\r') + draw_res[11].strip('\r')
            away = away_res[1].strip('\r') +  away_res[4].strip('\r') + away_res[6].strip('\r') + away_res[7].strip('\r') + away_res[10].strip('\r') + away_res[11].strip('\r')
            print(home)   #字符串，写入时需要拆开
            print(draw)
            print(away)
            print(url)
        except:
            print('数据缺失！')
            print(url)
        
        
        
if __name__ == '__main__':
    a = get_jishi()
    print(a)