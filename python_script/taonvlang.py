# -*- coding: utf-8 -*-
#导入库
import urllib.request
import re
import time
import urllib.error
#模拟浏览器
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0')]    
urllib.request.install_opener(opener)
for i in range(1,20):   #设定要爬取的页数
    url = 'https://mm.taobao.com/alive/list.do?scene=all&page='+str(i)   #构造网址  
    imgdata = urllib.request.urlopen(url).read().decode('utf-8','ignore')
    #使用正则表达式提取图片网址
    imgurl_list = re.compile('"avatarUrl":"(.*?)","darenNick"',re.S).findall(imgdata)
    for j in range(0,len(imgurl_list)):
        try:    #异常处理
            imgurl = imgurl_list[j]
            if 'img.alicdn.com' in imgurl:    #判断怎么构造图片链接
                img = 'http:' + imgurl
            else:
                img = imgurl + '_468x468q75.jpg'
            file = 'filepath' + str(i) + '-' + str(j) + '.jpg'
            urllib.request.urlretrieve(img,filename = file)    #使用urlretrieve直接写入       
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print(e.code)
            if hasattr(e,"reason"):
                print(e.reason)
            time.sleep(2)
        except Exception as e:
            print("exception:"+str(e))
            time.sleep(1)     
