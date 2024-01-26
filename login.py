from selenium import webdriver
import time
# 缺少验证码的情况
url = "https://www.douban.com"
web = webdriver.Chrome()
web.implicitly_wait(3)   # 隐式等待3秒
web.get(url)	# 链接到豆瓣首页
iframe = web.find_element_by_tag_name('iframe')     # 主代码在iframe里面，要先切进去
web.switch_to.frame(iframe)  # 切到内层
web.find_element_by_css_selector('.account-tab-account').click()    # 模拟鼠标点击
web.find_element_by_css_selector('#username').send_keys('15229970729')  # 模拟键盘输入
web.find_element_by_css_selector('#password').send_keys('hhh0123')
web.find_element_by_css_selector('.btn-account').click()
time.sleep(3)   # 要先等待，再获取源代码，否则获取的网页源代码是豆瓣首页
html = web.page_source  # 获取源代码

print("hhh000" in html)		# 你自己的账号名称，如果结果为True，则登录成功！（记得改成自己账号哦！）

web.quit()	# 关闭浏览器