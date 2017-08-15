# -*- coding: utf-8 -*-
"""
Created on Mon Aug 07 23:27:50 2017
对淘宝店铺数据进行抓取
@author: Administrator
"""
import requests
import re
import csv

keywork = input('请输入要搜索的关键字:')
url = 'https://s.taobao.com/search'
payload = {'q': keywork,'s': '1','ie':'utf8'}  #字典传递url参数
file = open('taobao_test.txt','w',encoding='utf8')
with open("result.csv", "w", newline="") as datacsv:
    csvwriter = csv.writer(datacsv, dialect=("excel"))
    csvwriter.writerow(['编号','标题','店铺名','掌柜名','地址','商品网站'])

    for k in range(0,1):        #100次，就是100个页的商品数据

        payload ['s'] = 44*k+1   #此处改变的url参数为s，s为1时第一页，s为45是第二页，89时第三页以此类推
        resp = requests.get(url, params = payload)
        print(resp.url)          #打印访问的网址
        resp.encoding = 'utf-8'  #设置编码
        title = re.findall(r'"raw_title":"([^"]+)"',resp.text,re.I)  #书名
    #    price = re.findall(r'"view_price":"([^"]+)"',resp.text,re.I) #价格
        loc = re.findall(r'"item_loc":"([^"]+)"',resp.text,re.I) #地址
    #    nick = re.findall(r'"nick":"([^"]+)"',resp.text,re.I) #店铺名
        id = re.findall(r'"nid":"([^"]+)"',resp.text,re.I) #用户ID
        x = len(title)           #每一页商品的数量
        for i in range(0,x) :    #把列表的数据保存到文件中
            r = requests.get(url='https://detail.tmall.com/item.htm?id='+id[i])
            storename = re.findall(r'<div class="tb-shop-name">[.\n].*?<dl>[.\n].*?<dd>[.\n].*?<strong>[.\n].*?<a href=.*?title="(.*?)"',r.text)
            usernames = re.findall(r'<div class="tb-shop-seller">[.\n].*?<dl>[.\n].*?</dt>[.\n].*?<dd>[.\n].*?[.\n].*?title="(.*?)">',r.text)
            if len(storename)>0:
                nick = storename[0]
                username = usernames[0].replace('掌柜:','')
            else:
                storename = re.findall(r'<a class="slogo-shopname.*?strong>(.*?)</strong>',r.text)
                if len(storename) > 0:
                    nick = storename[0]
                    username =nick
            print(nick)
            print(username)
        #file.write('编号:'+str(k*44+i+1)+'\n'+'标题：'+title[i]+'\n'+'店铺名:'+nick+'\n'+'掌柜名:'+username+'\n'+'地址：'+loc[i]+'\n'+'商品网址:'+'https://detail.tmall.com/item.htm?id='+id[i]+'\n'+'\n\n')

            csvwriter.writerow([str(k*44+i+1), title[i], nick, username,loc[i],'https://detail.tmall.com/item.htm?id='+id[i]])

#file.close()
