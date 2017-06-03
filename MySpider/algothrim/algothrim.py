# encoding=utf-8

import pymysql
import Block
import random

relation = None
max_int = None


supporters = []
againsters = []

def fetch_data():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="pentatonix0215",
                           charset="utf8mb4", db="spider")

    cur = conn.cursor()
    sql = "SELECT * FROM datas_second WHERE flag = 1 ORDER BY retweet DESC"
    cur.execute(sql)
    blocks = cur.fetchall()
    for x in blocks:
        block = Block.block()
        block.id = x[0]
        block.username = x[1].decode("utf-8")
        block.content = x[2].decode("utf-8")
        block.retweet = x[3]
        block.flag = x[4]
        supporters.append(block)
    sql = "SELECT * FROM datas_second WHERE flag = -1 ORDER BY retweet DESC"
    cur.execute(sql)
    blocks = cur.fetchall()
    for x in blocks:
        block.id = x[0]
        block.username = x[1].decode("utf-8")
        block.content = x[2].decode("utf-8")
        block.retweet = x[3]
        block.flag = x[4]
        againsters.append(block)

    set_range(againsters)
    set_range(supporters)

def set_range(blocks):
    i = -1
    for block in blocks:
        start = i
        end = start + block.retweet
        i = end
        block.range = {"start": start, "end": end}
    global  max_int
    max_int = i


def connect(id1, id2):
    global  relation
    relation = {id1 : id2, id2 : id1}


def compute_randwalk():
    percent = 0
    for i in range(0, 10000):
        global max_int
        number = random.randint(0, max_int)
        global supporters
        for supporter in supporters:
            end = supporter.range.get("end")
            if number < end:
                global  relation
                if_connected = relation.get(supporter.id)
                if if_connected is not None:
                    percent = percent + 1
                break;
    return float(percent)/10000


fetch_data()
connect(supporters[0].id, againsters[0].id)
print compute_randwalk()
connect(supporters[len(supporters) - 1].id, againsters[0].id)
print compute_randwalk()