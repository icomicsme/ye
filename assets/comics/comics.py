# -*- coding: UTF-8 -*-

# 理由Selenium库爬取漫画网站
# 并将漫画保存到本地
# 爬取的地址是：http://comic.sfacg.com/
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from urlparse import parse
import string
import requests
import sys
import time

# 使得 sys.getdefaultencoding() 的值为 'utf-8'
reload(sys)                      # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'

def mkdir(path):
    # '''
    # 防止目录存在
    # '''
    if not os.path.exists(path):
        os.mkdir(path)


def SavePic(filename, url):
    # '''
    # 通过requests库
    # 将抓取到的图片保存到本地
    # '''
    content = requests.get(url).content
    with open(filename, 'wb') as f:
        f.write(content)
def now():
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return nowTime

def get_TOF(index_url):
    # '''
    # 获取漫画的目录中的每一章节的url连接
    # 并返回一个字典类型k：漫画名 v：章节链接
    # '''
    url_list = []


    print('indexUrl:', index_url)
    # 模拟浏览器并打开网页
    chrome_options = Options()


    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('-–disable-javascript')
    chrome_options.add_argument('-–disable-plugins')
    chrome_options.add_argument('-–proxy-pac-url=https://wmtok.com/xfcdxg_zq/9478952.pac')


    # chrome_options.add_argument('--user-agent=mozilla/5.0 (macintosh; intel mac os x 10_12_6) applewebkit/537.36 (khtml, like gecko) chrome/68.0.3440.106 safari/537.36')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    print('begin get link', now())
    # browser.set_page_load_timeout(5)
    # browser.set_script_timeout(5)
    browser.get(index_url)
    print('end get link ', now())
    browser.implicitly_wait(3)


    # 找到漫画标题 并创建目录
    title = browser.title.split('-')[0]
    print('title', title)
    mkdir(title)

    # 找到漫画章节，注意，漫画可能会有多种篇章
    # 例如番外，正文，短片等等
    comics_lists = browser.find_elements_by_class_name('chapter-list')
    print('comics_lists:', comics_lists)
    # 寻找、正文等
    for part in comics_lists:
        # 找到包裹链接的links
        links = part.find_elements_by_tag_name('a')
        # 找到每个单独的章节链接
        for link in links:
            url_list.append(link.get_attribute('href'))

    # 关闭浏览器
    browser.quit()

    Comics = dict(name=title, urls=url_list)

    return Comics

def get_pic(Comics):
    # '''
    # 打开每个章节的url，
    # 找到漫画图片的地址，
    # 并写入到本地
    # '''
    comic_list = Comics['urls']
    basedir = Comics['name']

    print(basedir, comic_list)

    # browser = webdriver.PhantomJS()
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser.get(index_url)
    # browser.implicitly_wait(3)

    for url in comic_list:
        print('content url', url)
        browser.get(url)
        browser.implicitly_wait(3)

        # 创建章节目录
        dirname = basedir + '/' + browser.title.split('-')[1]
        mkdir(dirname)

        # 找到该漫画一共有多少页
        pageNum = browser.find_elements_by_class_name('manga-page')[0].text
        pageNum = int(pageNum.split('/')[1].replace('P', ''))
        print('pageNum', pageNum)

        # 找到下一页的按钮
        # nextpage = browser.find_element_by_xpath('//*[@id="AD_j1"]/div/a[4]')
        # nextpage = browser.find_element_by_id('action').find_elements_by_tag_name('li')[2] #.find_elements_by_tag_name('a')[0]
        # print('nextpage', nextpage, nextpage.get_attribute('offsetTop'))
        # 找到图片地址，并点击下一页
        for i in range(pageNum):

            # pic_url = browser.find_element_by_id('curPic').get_attribute('src')
            pic_url = browser.find_element_by_id('manga').find_elements_by_tag_name('img')[0].get_attribute('src')
            filename = dirname + '/' + str(i) + '.png'
            SavePic(filename, pic_url)
            # 点击下一页的按钮，加载下一张图

            browser.execute_script("document.body.removeChild(document.querySelector('#main01'))","")
            nextpage = browser.find_element_by_id('action').find_elements_by_tag_name('li')[2] #.find_elements_by_tag_name('a')[0]
            nextpage.click()
            # browser.execute_script("document.querySelectorAll('#action li a')[2].click()")
        print('当前章节{}  下载完毕'.format(browser.title))

    browser.quit()
    print('所有章节下载完毕')

# "http://manhua.sfacg.com/mh/YULINGSHI/"
def main():
    # url = str(input('请输入漫画首页地址： \n'))
    url = "https://m.k886.net/comic/name/%E7%A4%BE%E7%95%9C%E8%88%87%E5%86%B0%E6%B7%87%E6%B7%8B%E5%90%9B/id/35898"
    # url = "https://m.k886.net/comic/name/HMate/id/33422"
    # url = "https://m.k886.net/"
    # url = "http://manhua.sfacg.com/mh/YULINGSHI/"
    # url = quote(url, safe=string.pritable)
    Comics = get_TOF(url)
    get_pic(Comics)


if __name__ == '__main__':
    main()
