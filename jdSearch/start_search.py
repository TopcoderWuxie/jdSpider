#coding: utf-8

import sys
import time
import datetime
import threading
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data_save import DataSave
from config import TIME_WAIT, BaseUrl
from log_save import logging_save, Init

try:
    filename = __file__.split("\\")[-1].split(".")[0]
except Exception as e:
    filename = __file__.split("/")[-1].split(".")[0]

def search(url, shop_name):
    driver = webdriver.Chrome()
    try:
        driver.set_window_size(800,600)

        driver.get(url)
        driver.find_element_by_id("keyword").send_keys(shop_name)
        driver.find_element_by_class_name("input_submit").click()
        time.sleep(2)

        # threads = []
        count = 1
        while True:
            print("获取第%d页的商品链接" % count)
            move_mouse(driver)

            # _find_elements_by_xpath 函数不涉及到内存共享，只是处理每一页的数据，所以在这里开了多线程
            thread = threading.Thread(target= _find_elements_by_xpath, args= (driver, count))
            # threds.append(thread)
            thread.start()
            thread.join()

            # _find_next_page 函数中的driver要在下次循环中继续使用，所以这里并没有开多线程
            driver, flag = _find_next_page(driver)
            if flag == False:
                break
            count += 2

        # # 执行线程队列
        # runThreads = []
        # maxThread = 5
        # while threads or runThreads:
        #     for thread in runThreads:
        #         if not thread.is_alive():
        #             runThreads.remove(thread)

        #     while len(runThreads) < maxThread and threads:
        #         thread = threads.pop()
        #         thread.start()
        #         thread.join()
        #         runThreads.append(thread)
    finally:
        data.write() # 写入数据
        driver.quit()

def move_mouse(driver):
    """
    Note: 在该模块的开头加上了refresh方法，如果不加的话会报这种错误：selenium.common.exceptions.StaleElementReferenceException
    解决思路如下：https://huilansame.github.io/huilansame.github.io/archivers/exceptions-StaleElementReferenceException
    """
    driver.refresh() 

    #定位元素的初始位置
    start_point = WebDriverWait(driver, TIME_WAIT).until(
        EC.presence_of_element_located((By.NAME, "Keywords"))
    )

    #定位元素要移动到的目标位置
    end_point = WebDriverWait(driver, TIME_WAIT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pn-break"))
    )

    #执行元素的移动操作
    ActionChains(driver).drag_and_drop(start_point, end_point).perform()

def _find_elements_by_xpath(driver, count):
    try:
        WebDriverWait(driver, TIME_WAIT).until(
                # 查看第31个li标签不是加载出来了，如果加载出来了，证明接下来的30个商品成功加载
                EC.presence_of_element_located((By.XPATH, "//*[@id='J_goodsList']/ul/li[31]"))
                # EC.visibility_of_element_located((By.XPATH, "//*[@id='J_goodsList']/ul/li[31]"))
            )
    except Exception as e:
        logging_save("- {} - 动态加载后30条数据出错 {}".format(filename, e), "ERROR")
        print("显式等待出错：", e)
    elements = driver.find_elements_by_xpath("//div[@id='J_goodsList']/ul[@class='gl-warp clearfix']/li[@class='gl-item']")
    getInfo(elements, count)

def _find_next_page(driver):
    """
    Note: 这里如果不加refresh的话，同样会出现move_mouse中出现的错误。
    由于页面是30个商品或者是60个商品的时候都能够获取到下一页的标签，所以这里又执行了一次刷新操作
    """
    try:
        driver.refresh()
        WebDriverWait(driver, TIME_WAIT).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='J_bottomPage']/span[@class='p-num']/a[@class='pn-next']"))
        )
        driver.find_element_by_class_name("pn-next").click()
        return driver, True
    except Exception as e:
        logging_save("- {} - {}".format(filename, "页面爬取结束"), "ERROR")
        return driver, False

def getInfo(elements, count):
    num = 0
    for element in elements:
        try:
            href = element.find_element_by_xpath(".//div[@class='p-img']/a").get_attribute("href")
            data.addData(href)
            print(href)
            num += 1
        except Exception as e:
            logging_save("- {} - 获取href出错 {}".format(filename, e), "ERROR")
            print("获取href出错：", e)
    logging_save("- {} - 第{}页共有商品{}件".format(filename, count, num), "INFO")
    print("第{}页共有商品{}件".format(count, num))

def main_search(shop_name):
    global data
    Init()
    logging_save("爬取开始时间为：{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ), "INFO")
    data = DataSave() # 初始化redis数据库
    search(BaseUrl, shop_name)
    logging_save("爬取结束时间为：{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ), "INFO")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("输入参数为：python start_search.py shop_name(商品名称)")
        sys.exit(-1)
    
    main_search(sys.argv[-1])