# encoding=utf-8
import algothrim.algothrim

res = algothrim.algothrim.fetch_data()
supporters = res.get("supporters")
againsters = res.get("againsters")
for supporter in supporters:
    print supporter.retweet

s_big_degree_v = supporters[0]
s_small_degree_v = supporters[len(supporters) - 1]
a_big_degree_v = againsters[0]
a_small_degree_v = againsters[len(againsters) - 1]
