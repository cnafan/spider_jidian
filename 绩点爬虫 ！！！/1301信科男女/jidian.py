# gotit 绩点查询
import re
import urllib.request
from filecmp import cmp

import requests
from bs4 import BeautifulSoup


def write(jidian, xh, name):
    local = "C:\\Users\\zhang\\Desktop\\jidian.txt"
    if len(name) == 0:
        return
    fout = open(local, 'a+', encoding='utf-8')
    fout.write(name[0])
    fout.write("(")
    fout.write(xh)
    fout.write("):")
    fout.write(jidian[0])
    fout.write("\n")
    fout.close()
    print("写入成功")


def getinfo(html):
    reg = r'(?<=<td scope="col" align="left" valign="middle" nowrap>&nbsp;)[\u4e00-\u9fa5]{2,3}(?=</td>)'
    imgre = re.compile(reg)
    list = imgre.findall(html)
    print(list)
    return list


def spider_jidian(url, xuehao):
    user_agent = ("Mozilla/5.0 (Windows NT 6.3; WOW64)"
                  "AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/42.0.2311.152 Safari/537.36 LBBROWSER")
    header = {
        'User-Agent': user_agent
    }
    postdata = {'xh': xuehao
                }
    s = requests.Session()
    r = s.post(url,
               data=postdata,
               headers=header
               )
    if r.status_code == 200:
        print("login successfully " + str(r.status_code))
        # write(r.text)
        return r.text
    else:
        print("login unsuccessfully")
        # write(r.text)


def spider_name(url, xuehao):
    user_agent = ("Mozilla/5.0 (Windows NT 6.3; WOW64)"
                  "AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/42.0.2311.152 Safari/537.36 LBBROWSER")
    header = {
        'User-Agent': user_agent,
        'Referer': 'http://210.44.176.116/cjcx/xhcx_login.html'
    }
    postdata = {'post_xingming': '',
                'post_xuehao': xuehao,
                'Submit': '提交'
                }
    s = requests.Session()
    r = s.post(url,
               data=postdata,
               headers=header
               )
    if r.status_code == 200:
        print("login successfully " + str(r.status_code))
        # write(r.text)
        return r.text
    else:
        print("login unsuccessfully")
        # write(r.text)


def getxh(xh):
    sum = int(xh) + 1
    xh = str(sum)
    return xh


def getjidian(html):
    reg = r'(?<=<strong>)\d*\.\d*(?=</strong>)'
    imgre = re.compile(reg)
    imagelist = imgre.findall(html)
    # imagelist=re.findall('src="(.+?\.jpg)" pic_ext',html,re.M)
    return imagelist


def sum(jidian, xh, name):

    if len(name) != 0:
        dict_sum[xh]=[name[0], jidian[0]]
    return dict_sum

def write_fin(list):
    local = "C:\\Users\\zhang\\Desktop\\jidian_fin.txt"
    fout = open(local, 'a+', encoding='utf-8')
    for i in list:
        fout.write(i[0]+"-")
        fout.write(i[1][0]+"-")
        fout.write(i[1][1]+"\n")
    fout.close()

if __name__ == '__main__':
    dict_sum={}

    url_jidian = "http://gotit.asia/score"
    url_name = 'http://210.44.176.116/cjcx/xhcx_list.php'
    xh = '13111202001'
    xh_male=list(range())
    for i in range(25):
        html_jidian = spider_jidian(url_jidian, xh)
        jidian = getjidian(html_jidian)

        html_name = spider_name(url_name, xh)
        name = getinfo(html_name)

        dict_sum= sum(jidian, xh, name)
        xh = getxh(xh)
    #print(sorted(dict_sum.items(), key=lambda d: d[1]))
    write_fin(sorted(dict_sum.items(), key=lambda dict_sum: dict_sum[1]))
