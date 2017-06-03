# encoding=utf-8

import pymysql
import Block

def fetch_data():
    datas = []
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="pentatonix0215",
                           charset="utf8mb4", db="spider")

    cur = conn.cursor()
    sql = "SELECT * FROM datas"
    cur.execute(sql)
    blocks = cur.fetchall()
    for x in blocks:
        b = Block.block(x[1].decode("utf-8"), x[0].decode("utf-8"))
        datas.append(b)
    return datas
for block in fetch_data():
    print block.content