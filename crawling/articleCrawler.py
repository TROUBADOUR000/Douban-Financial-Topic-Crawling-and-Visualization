import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from InterDB import InterDB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from snownlp import SnowNLP

def fetchArticles():
    ib = InterDB('financial.db')
    frame = ib.read_db("select * from Note")
    for _, irow in frame.iterrows():
        try:
            noteID = irow['n_no']
            url = 'https://www.douban.com/note/' + noteID
            options = webdriver.ChromeOptions()
            options.binary_location = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            driver.delete_all_cookies()
            driver.execute_script("window.scrollBy(0,1000)")
            # 使用WebDriverWait等待页面加载完成
            try:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, 'tab-contents'))
                WebDriverWait(driver, 10000).until(element_present)
            except Exception as e:
                print("等待页面加载超时:", str(e))
            # 等待一段时间，确保异步加载完成
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            title_element = soup.select_one('div.note-header-container h1')
            a_title = title_element.text.strip() if title_element else ''

            time_element = soup.select_one('div.note-header-container span.pub-date')
            raw_time = time_element.text.strip() if time_element else ''
            a_time = raw_time.split()[0]  # 选择第一个空格前的部分，即年月日
            # 查找地址元素   去掉括号
            address_element = soup.select_one('span.usercard-loc')
            a_address = address_element.text.strip('()') if address_element else ''

            # 查找 class 为 note 的元素
            # 找到最外层的div id="wrapper"
            wrapper_div = soup.find(id="wrapper")
            # 在wrapper_div中找到class为"article"的div
            article_div = wrapper_div.find("div", class_="article")
            # 在article_div中找到所有class为"note"的子孙节点
            note_elements = article_div.find_all(class_="note")
            # 获取所有class为"note"的子孙节点内的文本内容
            a_text_list = [note.get_text("\n", strip=True) for note in note_elements]
            a_text = ""
            # 输出结果
            for i, all_text in enumerate(a_text_list, 1):
                if all_text != "":
                    a_text = all_text
                    break

            a_sentiment = SnowNLP(a_text).sentiments

            # 获取分享的数量
            shared_element = soup.select_one('div.sharing-button a.lnk-sharing span.rec-num')
            a_shared_str = shared_element.text.strip() if shared_element else ''
            a_shared = int(a_shared_str) if a_shared_str.isdigit() else 0  # 转换为整数，如果无法转换，则默认为0

            # 常见不突出重点的词
            english_stop_words = {'a', 'an', 'the', 'and', 'or', 'is', 'am', 'are', 'was', 'were', 'I', 'you', 'he',
                                  'she',
                                  'it', 'we', 'they', 'this', 'that', 'these', 'those', 'with', 'without', 'in', 'on',
                                  'at',
                                  'by', 'for', 'to', 'of', 'about', 'from', 'as', 'into', 'and', 'many', 'more'}
            chinese_stop_words = {'的', '了', '和', '是', '在', '有', '也', '又', '或', '而', '这', '那', '这些',
                                  '那些', '对',
                                  '与', '向', '和', '或者', '一些', '一种', '一样', '一般', '例如', '之类', '之一',
                                  '之间',
                                  '什么', '怎么', '多少', '哪里', '怎样', '怎么办', '为什么', '等等'}
            additional_stop_words = {'有', '吃', '上', '下', '左', '右', '说', '像', '用', '要', '没', '不', '见', '我',
                                     '会', '能够', '可以', '可能', '时候', '知道', '东西', '比如', '应该', '出来', '看到',
                                     '觉得', '发现', '确认', '问题', '一家', '人们', '认为', '作为', '大爷', '起来', '一身',
                                     '有的'}
            all_stop_words = english_stop_words.union(chinese_stop_words, additional_stop_words)
            s = SnowNLP(re.sub(r'[^\u4e00-\u9fa5a-zA-Z]', '', a_text))
            keywords = [word for word, tag in s.tags if tag in ['n', 'v'] and
                        all(stop_word not in word for stop_word in all_stop_words) and len(word) >= 2]
            a_keywords = ",".join(keywords)

            ib.insert_db_artical(a_title,a_text,a_time,a_address,a_keywords,a_shared,a_sentiment)

            # 输出标题
            print(f"a_title: {a_title}")

            # 关闭浏览器窗口
            driver.quit()
        except Exception as err:
            print(err)
            print("End Topic : index " + str(_) + "\n" + "name " + irow['n_name'] + "\n")


if __name__ == "__main__":
    fetchArticles()
