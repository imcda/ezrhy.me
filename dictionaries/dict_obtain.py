# -*- coding: utf-8 -*-
# Author : Han
# Time   : 03/08/2017
# Email  : klay.zhanghan@gmail
# Link   : https://github.com/Entheos1994

import urllib2
from bs4 import BeautifulSoup
import os
import requests
import sys

base_url = "http://pinyin.sogou.com"
category_url = "/dict/cate/index/"

def print_index():
    f = open('categories.txt', 'r')
    content = f.readlines()
    for line in content:
        print line

class Download():
    def __init__(self):
        self.category = None
        self.page = None
        self.category_dict = {'167': '城市信息', '1': '自然科学', '76': '社会科学',
                         '96': '工程应用', '127': '农林渔畜', '436': '电子游戏',
                         '154': '艺术设计', '389': '生活百科', '367': '运动休闲',
                         '31': '人文科学'}

        self.page_dict = {'167':10, '1':32, '76':51,
             '96':84, '127':10, '436':115, '154':20,
             '389':87, '367':18, '31':109}

    def _pagelink(self, cur_cate):
        url = base_url + category_url + str(cur_cate)
        page_url = url + '/default/' + str(self.page)
        print page_url
        req = urllib2.urlopen(page_url)
        if req.getcode() == 200:
            pass
        else:
            return 'not a valid categories'
        html  = req.read()

        # urls = base_urls + category
        soup  = BeautifulSoup(html, features="html5lib")
        sub_list = soup.find("div", {"id" : "dict_detail_list"})
        item_list = sub_list.find_all("div", {"class": "detail_title"})

        self.link_list = []
        for item in item_list:
            self.link_list.append(item.select("a")[0].attrs["href"])
        print ('returning page links'+'.'*10 +'\n') + ('category code: %s '%(cur_cate)) + (' page:%s'%(self.page))
        return self.link_list

    def _downloadlink(self, ctg_index):
        ctg_url = base_url + ctg_index
        ctg_html = urllib2.urlopen(ctg_url).read()
        soup = BeautifulSoup(ctg_html, features='html5lib')
        download_detail = soup.find('div', {'id':"dict_dl_btn"}).select("a")[0].attrs["href"]

        return download_detail

    def _download(self, link, cate):
        if len(link) == 0:
            return 'call pagelink first'

        # for link in self.link_list:
        detail = self._downloadlink(link)

        response = requests.get(detail, stream=True)
        headers = response.headers['Content-Disposition'].split('=')[1].strip('"')
        path = './'+str(cate)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(str(cate)+'/'+headers, 'wb') as handle:
            handle.write(response.content)
        print '> file stored: ' + str(link)
        return

def i_pipe(Down_object):
    input_index = sys.argv[1]
    if input_index == 'all':
        Down_object.category = Down_object.category_dict.keys()
        print 'indexes for all categories initilized'
        return Down_object
    elif input_index not in Down_object.category_dict.keys():
        print "> please enter a valid category index"
        os._exit(0)
    else:
        Down_object.category = [input_index]
        print 'index for %s'%(input_index) +' initialized'
        return Down_object

def p_pipe(Down_object, cate):
    input_pages = sys.argv[2]
    if input_pages == 'all':
        Down_object.pages = range(1, Down_object.page_dict[cate]+1)
        print 'pages initilized'
        return Down_object
    elif int(input_pages) < 0 or int(input_pages) > Down_object.page_dict[cate]:
        print '> please enter a valid category pages between 1 and %d'%(Down.page_dict[input_index])
        os._exit(0)
    else:
        Down_object.page = input_pages
        return Down_object


if __name__ == '__main__':
    Down = Download()
    i_pipe(Down)
    # p_page(Down)
    for cate_index in Down.category:
        print 'parsing %s'%(Down.category_dict[cate_index])
        p_pipe(Down, cate_index)
        if type(Down.page) != list:
            print 'parsing %s'%(Down.page) + ' th page download information'
            link_list = Down._pagelink(cate_index)
            for link in link_list:
                Down._download(link,cate_index)
        else:
            for line in Down.page:
                print 'download page %d ' % (line) + ' for category %s' % (Down.category_dict[cate_index])
                link_list = Down._pagelink()
                for link in link_list:
                    Down._download(link)

    print 'download compeleted'
    print 'files will be stored in ./category/dict_name.scel'
    print '.' * 20













