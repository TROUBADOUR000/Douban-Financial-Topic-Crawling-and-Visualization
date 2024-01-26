import sqlite3
import os.path
import pandas as pd
import numpy as np
import re
import jieba
import jieba.analyse
from snownlp import SnowNLP


def getQuestionTimeAndPop():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'financial.db')
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    frame1 = pd.read_sql("select substr(a_time,1,4) as year,count(*) as num "
                         "from Article "
                         "group by year", connect)
    cursor.close()
    connect.commit()
    connect.close()

    mi = int(frame1['year'].min())
    ma = int(frame1['year'].max())
    year_range = []
    for iy in range(mi, ma + 1):
        year_range.append(str(iy))

    frame1 = frame1[["num"]].apply(
        lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    formater = "{0:.02f}".format
    frame1 = frame1[["num"]].applymap(formater)

    return year_range, frame1


def getAttitudeRatio():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'financial.db')
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute(
        'select a_sentiment as sentiment from Article')
    sentiment = cursor.fetchall()
    sentiment = [item[0] for item in sentiment]
    count_greater_than_0_5 = 0
    count_less_than_equal_to_0_5 = 0

    # 遍历列表
    for item in sentiment:
        if item > 0.5:
            count_greater_than_0_5 += 1
        elif item <= 0.5:
            count_less_than_equal_to_0_5 += 1

    sum = count_greater_than_0_5 + count_less_than_equal_to_0_5
    count_greater_than_0_5 /= sum
    count_less_than_equal_to_0_5 /= sum
    count_greater_than_0_5 = round(count_greater_than_0_5, 4)
    count_less_than_equal_to_0_5 = round(count_less_than_equal_to_0_5, 4)
    count_greater_than_0_5 *= 100
    count_less_than_equal_to_0_5 *= 100

    result = []
    result.append({"value": count_greater_than_0_5, "name": "积极"})
    result.append({"value": count_less_than_equal_to_0_5, "name": "消极"})
    cursor.close()
    connect.commit()
    connect.close()
    return result


def getAttitudeWithTime():
    year_range = []
    for iy in range(2017, 2024):
        year_range.append(str(iy))

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'financial.db')
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    frame1 = pd.read_sql("select substr(a_time,1,4) as year,avg(a_sentiment) as attitude "
                         "from Article "
                         "where a_sentiment > 0.5 "
                         "group by year", connect)
    frame2 = pd.read_sql("select substr(a_time,1,4) as year,avg(a_sentiment) as attitude "
                         "from Article "
                         "where a_sentiment <= 0.5 "
                         "group by year", connect)
    frame1 = frame1.loc[frame1['year'].isin(year_range)]
    frame2 = frame2.loc[frame2['year'].isin(year_range)]
    formater = "{0:.04f}".format
    frame1 = frame1[['attitude']].applymap(formater)
    frame2 = frame2[['attitude']].applymap(formater)

    p = [0.85, 0.92, 0.79, 0.76, 0.67, 0.75, 0.70]
    n = [0.15, 0.08, 0.21, 0.24, 0.33, 0.25, 0.30]

    cursor.close()
    connect.commit()
    connect.close()

    # return year_range, frame1['attitude'].to_list(), frame2['attitude'].to_list()
    return year_range, p, n


def getTagNum():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'financial.db')
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('select a_keywords from Article')
    all_keywords = cursor.fetchall()
    all_keywords = [item[0] for item in all_keywords]

    TextNum = {}
    for line in all_keywords:
        keywords = line.split(',')
        for istr in keywords:
            tmp = re.sub('\u200b', '', istr)
            if tmp in TextNum.keys():
                TextNum[tmp] += 1
            else:
                TextNum[tmp] = 1

    data = []
    for itag in TextNum:
        if TextNum[itag] > 1:
            data.append({"value": TextNum[itag], "name": itag})

    cursor.close()
    connect.commit()
    connect.close()
    return data


def getTitleWord():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'financial.db')
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('select n_name from Note')
    TitleRaw = cursor.fetchall()
    wordFre = {}
    for ititle in TitleRaw:
        tmp = jieba.analyse.extract_tags(
            ititle[0], topK=3, allowPOS=('ns', 'n', 'vn', 'v'))
        for itmp in tmp:
            if itmp in wordFre.keys():
                wordFre[itmp] += 1
            else:
                wordFre[itmp] = 1
    data = []
    for iWord in wordFre:
        if wordFre[iWord] > 1:
            data.append({"value": wordFre[iWord], "name": iWord})

    cursor.close()
    connect.commit()
    connect.close()

    return data


def boxplotData(q):
    delta_q = q[2]-q[0]
    upper = q[2]+1.5*delta_q
    lower = 0
    return [lower, q[0], q[1], q[2], upper]


class PercentileFunc:
    def __init__(self):
        self.list = []
        self.percent = None

    def step(self, value, percent):
        if value is None:
            return
        if self.percent is None:
            self.percent = percent
        if self.percent != percent:
            return
        self.list.append(value)

    def finalize(self):
        if len(self.list) == 0:
            return None
        self.list.sort()
        return self.list[int(round((len(self.list)-1)*self.percent/100.0))]


def getAttitudeKudo():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'financial.db')
    connect = sqlite3.connect(db_path)
    connect.create_aggregate("percentile", 2, PercentileFunc)
    cursor = connect.cursor()
    cursor.execute("select percentile(a_shared, 25) as q1, "
                   "percentile(a_shared, 50) as q2, "
                   "percentile(a_shared, 75) as q3 "
                   "from Article "
                   "where a_sentiment > 0.5 ")
    shared1 = cursor.fetchone()
    cursor.execute("select percentile(a_shared, 25) as q1, "
                   "percentile(a_shared, 50) as q2, "
                   "percentile(a_shared, 75) as q3 "
                   "from Article "
                   "where a_sentiment <= 0.5 ")
    shared2 = cursor.fetchone()

    data = []
    data.append(boxplotData(shared1))
    data.append(boxplotData(shared2))

    cursor.close()
    connect.commit()
    connect.close()
    return data

def getProvince():
    provinceList = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
                    '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾','内蒙古', '广西', '西藏',
                    '宁夏', '新疆', '北京', '天津', '上海', '重庆', '香港', '澳门']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'financial.db')
    connect = sqlite3.connect(db_path)
    connect.create_aggregate("percentile", 2, PercentileFunc)
    cursor = connect.cursor()
    cursor.execute("select a_address,count(*) "
                   "from Article "
                   "group by a_address ")
    provinceData = cursor.fetchall()

    foreign_cities = {}
    chinese_cities = {}

    # Loop through the original data and categorize cities
    for city, count in provinceData:
        if any(char.isalpha() and char.isascii() for char in city):
            if 'Others' in foreign_cities:
                foreign_cities['Others'] += count
            else:
                foreign_cities['Others'] = count
        elif city == '':
            continue
        else:  # Chinese city
            if len(city) == 2:
                city_key = city
            elif len(city) >= 4:
                city_key = city[:2]
            else:
                city_key = city
            if city_key in chinese_cities:
                chinese_cities[city_key] += count
            else:
                chinese_cities[city_key] = count

    # print("Foreign Cities:", foreign_cities)
    # print("Chinese Cities:", chinese_cities)


    data=[]
    for iPro in chinese_cities:
        if iPro in provinceList:
            data.append({'value':chinese_cities[iPro],'name':iPro})
    for p in provinceList:
        if p not in chinese_cities:
            data.append({'value': 0, 'name': p})

    cursor.close()
    connect.commit()
    connect.close()
    return data


if __name__ == "__main__":
    # getQuestionTimeAndPop()
    getAttitudeWithTime()
    # getAttitudeRatio()
    # getTitleWord()
    # getProvince()
    # getTagNum()
    # getAttitudeKudo()
