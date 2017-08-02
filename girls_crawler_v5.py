# -*- coding:utf-8 -*-

from selenium import webdriver
import time

import urllib
import urllib2
from bs4 import BeautifulSoup

from HTMLParser import HTMLParser

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def main():
    # ******************  selenium Operations ***********************

    driver = webdriver.Chrome()   # open with Chrome
    # driver.get("https://www.zhihu.com/question/35931586") # 你的日常搭配是什么样子？
    # driver.get("https://www.zhihu.com/question/61235373") # 女生腿好看胸平是一种什么体验？
    # driver.get("https://www.zhihu.com/question/28481779") # 腿长是一种什么体验？
    driver.get("https://www.zhihu.com/question/19671417")  # 拍照时怎样摆姿势好看？


    # ****************** Scroll to the bottom, and do it 10 times *********
    def execute_times(times):

        for i in range(times + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            try:
                driver.find_element_by_css_selector('button.QuestionMainAction').click()
                print "page" + str(i)
                time.sleep(1)
            except:
                break

    execute_times(5)


    result_raw = driver.page_source
    result_soup = BeautifulSoup(result_raw, 'html.parser')

    result_bf = result_soup.prettify()

    # ****************   Store raw data file   *****************************************
    with open("./output/rawfile/raw_result.txt", 'w') as girls:
        girls.write(result_bf)
    girls.close()
    print "Store raw data successfully!!!"

    # ****************   Find all nodes that we want   *****************************************
    with open("./output/rawfile/noscript_meta.txt", 'w') as noscript_meta:
        noscript_nodes = result_soup.find_all('noscript')
        noscript_inner_all = ""
        for noscript in noscript_nodes:
            noscript_inner = noscript.get_text()
            noscript_inner_all += noscript_inner + "\n"

        h = HTMLParser()
        noscript_all = h.unescape(noscript_inner_all)
        noscript_meta.write(noscript_all)

    noscript_meta.close()
    print "Store noscript meta data successfully!!!"

    # ****************   Store meta data of imgs  *****************************************
    img_soup = BeautifulSoup(noscript_all, 'html.parser')
    img_nodes = img_soup.find_all('img')
    with open("./output/rawfile/img_meta.txt", 'w') as img_meta:
        count = 0
        for img in img_nodes:
            if img.get('src') is not None:
                img_url = img.get('src')

                line = str(count) + "\t" + img_url  + "\n"
                img_meta.write(line)
                urllib.urlretrieve(img_url, "./output/image/" + str(count) + ".jpg")
                count += 1

    img_meta.close()
    print "Store meta data and images successfully!!!"

if __name__ == '__main__':
    main()
