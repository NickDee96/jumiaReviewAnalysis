import json
import requests as req
import pandas as pd
import random
from bs4 import BeautifulSoup as soup
import time


def getHeader():
    headers=(
            {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
            {'user-agent':'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'},
            {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
            {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
            {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
            {'user-agent':'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; http://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0'},
            {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'},
            {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'},
            {'user-agent':'Mozilla/5.0 (X11; od-database-crawler) Gecko/20100101 Firefox/52.0'},
            {'user-agent':'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.16) Gecko/20110323 Ubuntu/10.04 (lucid) Firefox/3.6.16'},
        )
    return random.choice(headers)




def RevFinder(url):
    ''' takes a Jumia products page and extracts the ratings as percentages 
    and number of reviews. Returns a pandas dataframe of Name,
    product identifier, link,ratings and reviews'''
    page=soup(req.get(url,headers=getHeader() ).text,'lxml')
    containers=page.findAll('div',{'class':'-gallery'})
    a=pd.DataFrame(columns=('Name','Brand','SKU','Link','Rating','Reviews'))
    for i in containers:
        try:
            id=i['data-sku']
            pLink=i.a['href']
            pName=i.findAll('span',{'class':'name'})[0].text.replace('"','')
            brand=i.findAll('span',{'class':'brand'})[0].text.strip()
            width=i.findAll('div',{'class':'stars'})[0]['style']
            rating=width.replace('%','').split(': ')[1]
            revs=i.findAll('div',{'class':'total-ratings'})[0].text
            for r in [('(',''),(')','')]:
                revs=revs.replace(*r)
            a=a.append({
                'Name':pName,
                'Brand':brand,
                'SKU':id,
                'Link':pLink,
                'Rating':int(rating),
                'Reviews':int(revs)}
                ,ignore_index=True)
        except (IndexError,KeyError):
            pass
    return a


def catScraper(url,pages):
    df1=pd.DataFrame(columns=('Name','Brand','SKU','Link','Rating','Reviews'))
    for j in range(1,pages+1):
        try:
            url=(url+'&page={}')
            url=url.format(j)
            d1=RevFinder(url)
            df1=pd.concat([df1,d1],ignore_index=True)
        except :
            url=(url+'&page={}')
            url=url.format(j)
            d1=RevFinder(url)
            df1=pd.concat([df1,d1],ignore_index=True)            
    return df1


df=catScraper('https://www.jumia.co.ke/smartphones/?sort=popularity&dir=desc',25)


df.to_csv('Smartphones.csv')

