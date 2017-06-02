# encoding:utf-8
import urllib2
import re
from bs4 import BeautifulSoup
from time import sleep
import pymysql
import sys
from pymysql.err import  InternalError
reload(sys)

# print sys.setdefaultencoding("ascii")
def spider_craw():
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US;rv:1.9.1.6)'
                      'Gecko/20091201 Firefox/3.5.6',
        'Cookie': 'UOR=baike.baidu.com,widget.weibo.com,login.sina.com.cn; '
                  'SINAGLOBAL=1295938907094.776.1491734990989; '
                  'ULV=1496370835311:12:4:8:1652963482545.7085.1496370835309:1496365588488; '
                  'UM_distinctid=15b529dfcd17e-096eccbb6e0e37-47534130-1fa400-15b529dfcd244a; '
                  'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5fhzAnQW6FG7.QqpcEXMOR5JpX5KMhUgL.Fo'
                  '-ceKeNSon4eh52dJLoI7DQqPHrP02XSoe0; SUHB=04Wu03Rzs5Xgof; '
                  'SCF=AlmbOf2uF_HS52G1JMyD2Gj61uNWvU52DWm_xqvlj6HN3LtYEisy0cgUUxJVI-Ui2FOMPJMTVMrNfaZssmukTF8.; '
                  'ALF=1527906822; wvr=6; un=15600800736; SWB=usrmdinst_8; '
                  'SUB=_2A250NL7XDeRhGeNI6lEW9ibFyzyIHXVXQ5cfrDV8PUNbmtANLUjbkW9fFgCj1G1QYlJ3lNpMDNpAjsf7Pw..; '
                  'SSOLoginState=1496370823; WBStorage=02e13baf68409715|undefined; _s_tentry=login.sina.com.cn; '
                  'Apache=1652963482545.7085.1496370835309 '
    }
    data = ""
    for i in range(1, 30):
        url = 'http://s.weibo.com/weibo/TOP%25E5%2590%25B8%25E6%25AF%2592&page=' + str(i)
        request = urllib2.Request(url=url, headers=headers)
        page = urllib2.urlopen(request).read()
        data = data + page
        fh = open("G:\\text.txt", "w")
        fh.write(data)
        fh.close()
        sleep(2)
        parse()
def parse():
    fh = open("G:\\text.txt", "r")
    data = fh.read()
    fh.close()
    soup = BeautifulSoup(data, "lxml")
    divs = soup.select(".feed_content")
    fh = open("G:\\temp.txt", "a")
    data = ""
    for div in divs:
        for index, node in enumerate(div.children):
            flag = False
            if index == 1:
                data = data + "nickname:" + str(node["nick-name"]) + "\n"
            else:
                try:
                    children = node.children
                except AttributeError:
                    continue
                for child in children:
                    # if not flag:
                    reg_pointy = re.compile(r'<.*/.*>')
                    string = reg_pointy.search(str(child))
                    if string is None:
                        data = data + "content" + str(child) + "\n"

        print "--------------------------------------"
    fh.write(data)

def insert():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="pentatonix0215", db="spider", charset="utf8mb4")
    cur = conn.cursor()
    f = open("G:\\data.txt").read()
    reg_content = re.compile("name:([\d\D]+?)nick")
    content = reg_content.findall(f)
    list = []
    for index, one in enumerate(content):
        # 提取name
        reg_name = re.compile("(.+?)\n")
        name = reg_name.search(one).group(1)
        # 提取tex t
        reg_text = re.compile(".+?\n([\d\D]*)")
        text = reg_text.search(one).group(1)
        # 去掉content
        reg_content = re.compile("content")
        text = reg_content.sub("", text)
        text = text.encode("utf-8").encode("unicode-escape")
        # 去掉换行符、空格
        reg_n = re.compile("\\\\n")
        reg_t = re.compile("\\\\t")
        text = reg_n.sub("", text)
        text = reg_t.sub("", text)
        text = text.decode("unicode-escape")
        # 加入
        block = (index, name, text)
        list.append(block)
        print text, "--------------------------------"
    sql = "INSERT INTO datas(id,username,content) VALUES(%s,%s,%s)"
    try:
        cur.executemany(sql, list)
        conn.commit()
    except InternalError:
        pass


insert()
