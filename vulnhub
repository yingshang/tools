import requests
from bs4 import BeautifulSoup
import os
from contextlib import closing
import hashlib
import os

site = "https://www.vulnhub.com"
my_proxies = {"http": "http://127.0.0.1:1080", "https": "https://127.0.0.1:1080"}


def get_md5(file_path):
    f = open(file_path, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    return md5


def download(url, path, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    with closing(requests.get(url, headers=headers, stream=True, proxies=my_proxies)) as response:
        chunk_size = 8192  # 单次请求最大值
        content_size = int(response.headers['content-length']) / 1024 / 1024  # 内容体总大小
        data_count = 0
        with open(path + "\\" + filename, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data) / 1024 / 1024
                now_jd = (data_count / content_size) * 100
                print("\r 文件下载进度：%d%%(%dm/%dm) - %s" % (now_jd, data_count, content_size, filename), end=" ")


# def download(url,path,filename):
#     r = requests.get(url, stream=True, proxies=my_proxies)
#     f = open(path+"\\"+filename, "wb")
#     print('开始下载：'+url)
#
#     for chunk in r.iter_content(chunk_size=8192):  # 每次下载5120，因为我的大点，我选择每次稍大一点，这个自己根据需要选择。
#         if chunk:
#             f.write(chunk)
#     print(filename+'下载完成！！！')


for i in range(6, 38):
    print(str(i))
    url = "https://www.vulnhub.com/?page=" + str(i)
    r = requests.get(url=url, proxies=my_proxies)
    soup = BeautifulSoup(r.text, "lxml")
    ulists = soup.find_all('div', class_='span9 entry-title')

    for j in range(len(ulists)):
        donwload_urls = []
        url2 = site + ulists[j].a.get("href")
        title = ulists[j].a.string.replace(":", "-")
        path = "e:\\vulnhub\\" + title
        if not os.path.exists(path):
            os.makedirs(path)
        r2 = requests.get(url2, proxies=my_proxies)
        soup2 = BeautifulSoup(r2.text, "lxml")
        ulists2 = soup2.find_all('div', class_='accordion-inner')
        downlist = []
        lists = []

        for n in soup2.find_all("ul"):
            if n.find_all("li")[0].b == None:
                pass
            elif n.find_all("li")[0].b.string == "Download (Mirror)":
                download_url = n.find_all("li")[0].a.string
                downlist.append(download_url)
            elif n.find_all("li")[0].b.string == "Filename":
                filename = n.find_all("li")[0].text.replace("Filename: ", "")
                md5_sign = n.find_all("li")[2].text.replace("MD5: ", "")
                lists.append({filename: md5_sign})
        if len(downlist) == 0:
            ulists3 = soup2.find_all("li")
            for n in ulists3:
                try:
                    if n.b.string == "Download (Mirror)":
                        downlist.append(n.a.string)
                except AttributeError:
                    pass

        for download_url in downlist:
            filename = download_url.split("/")[-1]
            for i in lists:
                try:
                    md5_sign = i[filename].lower()
                except KeyError:
                    pass

            if os.path.exists(path+"\\"+filename):
                md5 = get_md5(path+"\\"+filename)
                while md5 != md5_sign:
                    print(md5_sign)
                    print(md5)
                    if md5 == "1e1a0d3eb9998c8d736a6dea72d244ee":
                        break
                    download(url=download_url, path=path, filename=filename)
                    md5 = get_md5(path + "\\" + filename)
            else:
                download(url = download_url,path=path,filename=filename)


        # for k in range(len(ulists2)):
        #     try:
        #         for n in range(len(ulists2[k].find_all("ul"))):
        #             #print(ulists2[k].find_all("ul")[n])
        #             for l in range(len(ulists2[k].find_all("ul")[n].find_all("li"))):
        #
        #                 #if ulists2[k].find_all("ul")[n].find_all("li")[l].b.string == "MD5":
        #                 #    md5_sign = ulists2[k].find_all("ul")[n].find_all("li")[l].text.replace("MD5: ","")
        #                 #    print(md5_sign)
        #                 if  ulists2[k].find_all("ul")[n].find_all("li")[l].b.string  =="Download (Mirror)":
        #                     download_url = ulists2[k].find_all("ul")[n].find_all("li")[l].a.string
        #                     filename = download_url.split("/")[-1]
        #                     if os.path.exists(path+"\\"+filename) ==False:
        #                         download(url = download_url,path=path,filename=filename)
        #     except AttributeError:
        #         pass
