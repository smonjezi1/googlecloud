from craigslist import CraigslistJobs, CraigslistForSale
import time
import pandas as pd
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
import requests
import re

page= requests.get('https://geo.craigslist.org/iso/us')
soup = BeautifulSoup(page.text, "lxml")
links =[]
a=soup.find_all(lambda tag: tag.name == 'li')
for tag_a in a:
    link_a=tag_a.find_all('a')
    if link_a!=[]:            
        link_b=link_a[0]
        links.append(link_b['href'])
cities=[]
for link in links:
    try:
        city = re.findall(r'^https:\/\/([^>]*)\.craigslist.org', link)[0]
    except:
        continue        
    if city in ['forums','','www']: continue
    cities.append(city)

conn = sqlite3.connect(r"./carigslist_data_main.db")

start = time.time()

conn.execute('''CREATE TABLE newdata(City,Miles,ID,Name,Price,date,url,VIN,odometer,status,model)''')

for city in cities:
    print(city)
    for min_mls in list(range(5000,180000,1000)):
        cl_h = CraigslistForSale(site=city, category='cta',
                                 filters={'min_miles':min_mls, 'max_miles':min_mls+999,'min_price': 1500, 'max_price': 70000,'has_image':True})
        id_list=[]
        for i in cl_h.get_results():
            if i['name'] in id_list:
                continue
            id_list.append(i['name'])
            conn.execute("INSERT INTO newdata(City,Miles,ID,Name,Price,date,url,VIN,odometer,status, model) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                             (city,min_mls,i['id'],i['name'],i['price'], i['datetime'],i['url'],i['VIN'],i['odometer'],i['status'],i['model']))
        conn.commit()
conn.close()
end = time.time()
print(end - start)
#t=1621.0531091690063
