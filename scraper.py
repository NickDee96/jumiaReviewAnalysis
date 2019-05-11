import json
import requests as req
from bs4 import BeautifulSoup as soup

def maxRevFinder(url):
    page=req.get(url,'lxml')
    containers=page.findAll('div',{'class':'-gallery'})
    for i in containers:
        id=i['data-sku']
        brand=i.findAll('span',{'class':'brand'})[0].text.strip()
        width=i.findAll('div',{'class':'stars'})[0]['style']
        rating=width.replace('%','').split(': ')[1]
        revs=i.findAll('div',{'class':'total-ratings'})[0].text
        for r in [('(',''),(')','')]:
            revs=revs.replace(*r)




page=soup(req.get('https://www.jumia.co.ke/smartphones/?sort=popularity').text,'lxml')
containers=page.findAll('div',{'class':'-gallery'})
width=containers[0].findAll('div',{'class':'stars'})[0]['style']
rating=width.replace('%','').split(': ')[1]

pName=containers[0].findAll('span',{'class':'name'})[0].text.replace('"','')
type(brand)