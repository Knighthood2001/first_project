import requests
import json
import re
import pandas as pd
url = 'https://pvp.qq.com/web201605/js/herolist.json'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
# print(response.text)
herolist = json.loads(response.text)
# print(herolist)
ename = []
for item in herolist:
    herolist_ename = item["ename"]
    ename.append(herolist_ename)
# print(ename)

base_url = "https://pvp.qq.com/web201605/herodetail/{}.shtml"
df = []

# 标题栏
columns = ['英雄', '被动', '一技能', '二技能', '三技能', '四技能']
a = 1
for i in ename:
    # print(i)
    true_url = base_url.format(i)
    r = requests.get(true_url, headers=headers)
    r.encoding = "gbk"
    names = re.compile('<label>(.*?)</label>')
    name = names.findall(r.text)[0]
    # 用来显示英雄个数
    print(str(a) + name)
    a += 1
    # 没有这个[0]，会使得excel中的数据是['云中君']，即中文名外面还有引号和[]
    skills = re.compile('<p class="skill-desc">(.*?)</p>', re.S)
    skill = skills.findall(r.text)
    # 数据清洗
    beid = skill[0]
    beidong = beid.replace("被动：", "")
    jineng1 = skill[1]
    jineng2 = skill[2]
    jineng3 = skill[3]
    jineng4 = skill[4]
    b = df.append([name, beidong, jineng1, jineng2, jineng3, jineng4])
    d = pd.DataFrame(df, columns=columns)
    # index=False表示输出不显示索引值
    d.to_excel("王者荣耀英雄与技能.xlsx", index=False)


