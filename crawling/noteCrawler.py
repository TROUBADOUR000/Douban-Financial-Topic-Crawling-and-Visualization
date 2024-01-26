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

# insert_db_note
def note_to_db(notes, ib):
    for note in map(str, notes):
        match = re.search(r'href="https://www.douban.com/note/(\d+)/" target="_blank">([^<]+)</a>', note)
        if match:
            no = match.group(1)
            name = match.group(2)
            print(f"no: {no}, name: {name}")
            ib.insert_db_note(name, no)
        else:
            print("未找到匹配的 href，跳过此记录")
            continue


def fetchNotes():
    ib = InterDB('financial.db')
    frame = ib.read_db("select * from Topic")
    for _, irow in frame.iterrows():
        try:
            topicID = irow['t_no']
            url = 'https://www.douban.com/channel/' + topicID
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
            time.sleep(10)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            tab_contents_div = soup.find('div', {'class': 'tab-contents'})
            if tab_contents_div:
                # 在 <div id="wrapper"> 下查找所有标题 <h2 class="title">
                notes = tab_contents_div.find_all('h2', {'class': 'title'})
                note_to_db(notes, ib)
            else:
                print("未找到 <div id='wrapper'> 元素")
            # 关闭浏览器窗口
            driver.quit()
        except Exception as err:
            print(err)
            print("End Topic : index " + str(_) + "\n" +
                  "name " + irow['t_name'] + "\n")


if __name__ == "__main__":
    fetchNotes()
