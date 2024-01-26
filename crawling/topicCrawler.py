import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from InterDB import InterDB
import json
from selenium import webdriver


class doubanTopicCrawler:
    def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/108.0.0.0 Safari/537.36",
                        'cookie': r"_zap=fec6e5e7-7763-43c3-9b75-dc538a893790; d_c0=AXCYQvlWARaPThyF1VfOMcPSIL10kFKNNtQ=|1670827030; YD00517437729195:WM_TID=6MqmPRd306hEUFQBRUOEYgb2aZ88REf5; YD00517437729195:WM_NI=yzAER2H+8oNXehktfBXDkg8bqkiptiKrnA1deVcXrru1dTS1idSNaMe7GAgq3pMfhCL0YYXtIobprgWYwXVgPDNgaKXuZkT9LXq0H8yLDxFNf0DmsOErRImLVlR7HZVza0U=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6ee96b143b895bb87bb4bf78a8ea7d45b838a9fb0d452afbea0d6d748a5bbb685eb2af0fea7c3b92abba68fa6d13a8cf5f890cd54a7b8a595e54a9c9ca588bb6ab3b5a791f76389aea2a2b470a78aadb9f17ab7efacb5d23babbc9dafe447a7e989a2e67bf1b08387eb4990f097badb808bb1ae91f16d9587b9b9d56d949c8288e4419cab968cd7339088bfd1cb34bb948c99c546a6f08c8ef24587ae9eaaf04896b49ed8cb5296a6afd1d837e2a3; captcha_session_v2=2|1:0|10:1672299344|18:captcha_session_v2|88:MVQyZEcySkQzQXExMklqd1pPTUdsNEsvUldJMGNhaXpIbUJDN0swNVJoTElSV2ZrRzlqZE9UaTZ0YSs1UDJzcQ==|a958c413aad900015524c1056772cf64f370470c6a6c6592386a3ffb6bd52b99; q_c1=9e691d8230044b13974c01470eb6aaf5|1672299394000|1672299394000; gdxidpyhxdE=7rJ33BIeigjUUOebDq3E7egmWmp8Sh35ZWm0srxGoonOTB57Rjl0hxnJ5Cdqwbz/Wi6SLba9TCyuvbUC7H4zcNtDBZPQZNOEE\xkwejhDhTGTACao3yBKjUrzfl04qTX+Cs5zP2+f2qeqjaU3ORKzSaDzXZbwQVg+3kkUms03u3pannB:1672324965245; z_c0=2|1:0|10:1672389751|4:z_c0|92:Mi4xbHVTcUh3QUFBQUFCY0poQy1WWUJGaGNBQUFCZ0FsVk5ncEdhWkFDdzRXVFp3bGMwbUVMbEUyUDRWRncwSmd4M0pB|a2353788b7f71922d4b6b2bafc7f9ed992c74b4545a4aedb7f340e495d8d6023; __utma=51854390.1969994280.1672548639.1672548639.1672548639.1; __utmz=51854390.1672548639.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20201005=1^3=entry_date=20201005=1; tst=r; _xsrf=87bbbc73-4ff7-4b48-83d4-f6e7c9064fa3; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1672477088,1672538562,1672622462,1672627415; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1672630090; ariaDefaultTheme=undefined; KLBRSID=d017ffedd50a8c265f0e648afe355952|1672630128|1672627414"}

        self.topicCode = {'理财': '30169671'}
        self.startUrl = "https://www.douban.com/channel/"
        self.questionType = ['']
        self.visited = []
        self.qu = ['理财']
        self.cookies = []

    def login_for_cookie(self, topicName):
        for iType in self.questionType:
            all_url = self.startUrl + self.topicCode[topicName] + iType
            options = webdriver.ChromeOptions()
            options.binary_location = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            driver = webdriver.Chrome(options=options)
            driver.get(all_url)
            input("enter after log in")
            self.cookies = driver.get_cookies()
            with open("cookies.json", "w", encoding="utf-8") as cks:  # 把cookies使用json保存
                json.dump(self.cookies, cks)

    def get_cookies(self):
        with open("cookies.json", "r", encoding="utf-8") as cks:  # 从json文件中获取之前保存的cookie
            self.cookies = json.load(cks)

    def spider_href(self, Topic_name, dataBase=None):
        if Topic_name not in self.topicCode.keys():
            print("Topic does not exist!")
            return
        all_url = self.startUrl + self.topicCode[Topic_name] + self.questionType[0]
        print("Accessing " + all_url + "...")
        self.visited.append(Topic_name)
        n = 0

        while (n < 5):
            flag = False
            try:
                options = webdriver.ChromeOptions()
                options.binary_location = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                self.driver = webdriver.Chrome(options=options)
                self.driver.get(self.startUrl + self.topicCode[Topic_name] + self.questionType[0])
                self.driver.delete_all_cookies()
                # self.get_cookies()
                # for i in self.cookies:
                  #  self.driver.add_cookie(i)
                self.driver.get(all_url)
                self.driver.execute_script("window.scrollBy(0,1000)")
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                print("*** ", n)
                # 找到相关频道模块
                related_channels_module = soup.find('div', {'id': 'related-channels'})
                # print(related_channels_module)
                # 找到其中的所有 <li> 元素
                li_elements = related_channels_module.find_all('li')
                for item in li_elements:
                    span_element = item.find('span')
                    if not span_element:
                        continue
                    try:
                        a_cover = item.find('a', class_='cover')
                        href = a_cover['href']
                        topic_no_match = re.search(r'/channel/(\d+)', href)
                        if topic_no_match:
                            topic_no = topic_no_match.group(1)
                        else:
                            topic_no = None

                        a_title = item.find('a', class_='title')
                        topic_name = a_title.text.strip()

                        # print(topic_no, ' * ', topic_name)

                        if topic_name:
                            flag = True

                        if topic_name not in self.visited:
                            self.qu.append(topic_name)
                            self.topicCode[topic_name] = topic_no
                            dataBase.insert_db_href(topic_name,topic_no)
                            print(topic_name)

                    except Exception as err:
                        print(err)
                if flag:
                    break

            except Exception as err:
                print(err)
                n += 1

    def bfs_search(self):
        max_nodes = 8
        i = 0
        ib = InterDB('financial.db')
        ib.open_db()
        ib.insert_db_href('理财', '30169671')
        all_topics = []
        while len(self.qu) != 0:
            org_topic = self.qu.pop()
            if org_topic not in self.visited:
                self.spider_href(org_topic, ib)
                print(org_topic)
                i += 1
                all_topics.append({'Topic_Name': org_topic, 'Topic_No': self.topicCode[org_topic]})
            if i > max_nodes:
                break

        ib.close_db()
        self.driver.close()
        # df = pd.DataFrame(all_topics, columns=['Topic_Name', 'Topic_No'])
        # df.to_csv('topics.csv', index=False, encoding='utf-8')


if __name__ == "__main__":
    ws = doubanTopicCrawler()
    # ws.login_for_cookie('理财')
    ws.bfs_search()
