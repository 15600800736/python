# encoding:utf-8
import urllib2
import re
from bs4 import BeautifulSoup
from time import sleep
import pymysql
from pymysql.err import InternalError
import algothrim.Block
list = []
files = ""
last_len = 0
def spider_craw():
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US;rv:1.9.1.6)'
                      'Gecko/20091201 Firefox/3.5.6',
        'Cookie': 'UOR=baike.baidu.com,widget.weibo.com,login.sina.com.cn; '
                  'SINAGLOBAL=1295938907094.776.1491734990989; '
                  'ULV=1496453286746:13:5:9:4213569759219.834.1496453286722:1496370835311; '
                  'UM_distinctid=15b529dfcd17e-096eccbb6e0e37-47534130-1fa400-15b529dfcd244a; '
                  'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5fhzAnQW6FG7.QqpcEXMOR5JpX5KzhUgL.Fo'
                  '-ceKeNSon4eh52dJLoI7DQqPHrP02XSoe0; SUHB=0idrflekB3CVGm; '
                  'SCF=AlmbOf2uF_HS52G1JMyD2Gj61uNWvU52DWm_xqvlj6HNryfA4IBUPcAoYxsTS35h1TZB4O0re8Yb59NQA05rbcY.; '
                  'ALF=1527989273; wvr=6; un=15600800736; '
                  'SUB=_2A250NmDKDeRhGeNI6lEW9ibFyzyIHXVXQtUCrDV8PUNbmtBeLUTBkW-C8msuo17CO-Fzgrn7ckcJG6s_nw..; '
                  'SSOLoginState=1496453273; _s_tentry=login.sina.com.cn; Apache=4213569759219.834.1496453286722; '
                  'SWB=usrmdinst_4; WBStorage=02e13baf68409715|undefined '
    }
    data = ""
    for i in range(1, 20):
        url = 'http://s.weibo.com/weibo/TOP%25E9%2581%2593%25E6%25AD%2589&page=' + str(i)
        request = urllib2.Request(url=url, headers=headers)
        page = urllib2.urlopen(request).read()
        global data
        data = page
        # print data
        sleep(5)
        parse(data)
        global  list
        if len(list) == last_len:
            print "has caught! index is:" + str(len(list) - 1)
            break;
        print str(i) + ":" + str(len(list))
        global  last_len
        last_len = len((list))
    insert()
i = 884         

def parse(data):
    # fh = open("F:\\text.txt", "r")
    # data = fh.read()
    # fh.close()
    soup = BeautifulSoup(data, "lxml")
    outers = soup.select(".WB_cardwrap")
    for outer in outers:

        # block = algothrim.Block.block()
        username = None
        content = ""
        retweet = None

        html = "<html><body>" + str(outer) + "</body></html>"
        outer_soup = BeautifulSoup(html, "lxml")
        # 提取转发数
        feed_actions = outer_soup.select(".feed_action_row4")
        for feed_action in feed_actions:
            html = "<html><body>" + str(feed_action) + "</body></html>"
            action_soup = BeautifulSoup(html, "lxml")
            lines = action_soup.select(".line")
            retweet_reg = re.compile("<em>([\d]*)</em>")
            retweet_nums = retweet_reg.findall(str(lines[1]))
            for retweet_num in retweet_nums:
                if retweet_num == "":
                    retweet = 0
                else:
                    retweet = retweet_num
        # 提取内容
        divs = outer_soup.select(".feed_content")
        # fh = open("F:\\temp.txt", "a")
        # data = ""
        for div in divs:
            for index, node in enumerate(div.children):
                if index == 1:
                    # data = data + "nickname:" + str(node["nick-name"]) + "\n"
                    username = str(node["nick-name"])
                else:
                    try:
                        children = node.children
                    except AttributeError:
                        continue
                    for child in children:
                        reg_pointy = re.compile(r'<.*/.*>')
                        string = reg_pointy.search(str(child))
                        if string is None:
                            content = content + str(child)
                    # 去掉换行符、空格
                    reg_n = re.compile("\\\\n")
                    reg_t = re.compile("\\\\t")
                    content = reg_n.sub("", content)
                    content = reg_t.sub("", content)
                    # content = content.decode("unicode-escape")
                    # data = data + "content" + str(child) + "\n"
                    # print "--------------------------------------"

        # block.username = username
        # block.content = content
        # block.retweed = retweet
        if username is not None:
            block = (i,username,content,retweet)
            global i
            i = i + 1
            global list
            list.append(block)
            # fh.write(data)


def insert():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="pentatonix0215", db="spider",
                           charset="utf8mb4")
    cur = conn.cursor()
    # f = open("F:\\temp.txt").read()
    # reg_content = re.compile("name:([\d\D]+?)nick")
    # content = reg_content.findall(f)
    # list = []
    # for index, one in enumerate(list):
        # 提取name
        # reg_name = re.compile("(.+?)\n")
        # name = reg_name.search(one).group(1)
        # 提取tex t
        # reg_text = re.compile(".+?\n([\d\D]*)")
        # text = reg_text.search(one).group(1)
        # 去掉content
        # reg_content = re.compile("content")
        # text = reg_content.sub("", text)
        # text = text.encode("utf-8").encode("unicode-escape")
        # 去掉换行符、空格
        # reg_n = re.compile("\\\\n")
        # reg_t = re.compile("\\\\t")
        # text = reg_n.sub("", text)
        # text = reg_t.sub("", text)
        # text = text.decode("unicode-escape")
        # 加入
        # block = (index, name, text)
        # list.append(block)
        # print text, "--------------------------------"
    sql = "INSERT INTO datas_second(id,username,content,retweet) VALUES(%s,%s,%s,%s)"
    # print len(list)
    # try:
    cur.executemany(sql, list)
    conn.commit()
    # except InternalError:
    #     pass
spider_craw()