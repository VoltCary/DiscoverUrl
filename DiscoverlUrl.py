#encoding=utf-8

import requests
from lxml import etree
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
import optparse



def _write(url):
    f=open('url.txt','a')
    f.write(url + '\n')

def baidu(keyword,page):
    L=[]
    url=('http://www.baidu.com/s?wd=%s&pn=%s') % (keyword,page)
    r=requests.get(url)
    p=etree.HTML(r.content)
    tags=p.xpath(u'//a[@class="c-showurl"]')
    for tag in tags:
        try:
            urll=tag.get('href')
            rr=requests.get(urll)
            soup = BeautifulSoup(rr.content, 'html.parser')
            title = soup.title.string
            if rr.url:
                print('[baidu] %s %s' % (rr.url,title))
                L.append(rr.url)
        except:
            pass
    return L

def _360(keyword,page):
    L=[]
    url=("https://www.so.com/s?q=%s&pn=%s&fr=so.com") % (keyword,page)
    r=requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    t=soup.select('a[rel="noopener"]')
    for i in t:
        if i["data-url"]:
            print('[360] %s %s' % (i["data-url"],i.string))
            L.append(i["data-url"])
    return L

def main(keyword,page):
    pool = Pool()
    #num=[x*10 for x in range(0,page)]
    num=[[keyword,page] for page in map(lambda x :x*10,range(page))]
    numm=[[keyword,page] for page in map(lambda x :x,range(page))]
    tmp_L=pool.starmap(baidu,num)
    for x in tmp_L:
        for a in x:
            _write(str(a))
    tmp_K=pool.starmap(_360,numm)
    for k in tmp_K:
        for t in k:
            print(t)
            _write(str(t))
    pool.close()
    pool.join()


if __name__=='__main__':

    banner='''
    ____  _                                ____  __     __
   / __ \(_)_____________ _   _____  _____/ / / / /____/ /
  / / / / / ___/ ___/ __ \ | / / _ \/ ___/ / / / / ___/ / 
 / /_/ / (__  ) /__/ /_/ / |/ /  __/ /  / / /_/ / /  / /  
/_____/_/____/\___/\____/|___/\___/_/  /_/\____/_/  /_/   
                                                         
                      Coded By VoltCary (v1.0 RELEASE)                          '''
                    
    
    print(banner)
    file=open('url.txt','w+')
    file.truncate()
    file.close()
    usage="usage %prog -p/-P <target pages>"
    parser=optparse.OptionParser(usage)
    parser.add_option('-P','-p', type="int", dest="page", default='10', help="search for page")
    parser.add_option('-K','-k', type="string", dest="keyword", default='', help="search for keywords")
    (options, args)=parser.parse_args()
    keyword=options.keyword
    page=options.page
    main(keyword,page)


