from bs4 import BeautifulSoup
from datetime import datetime
import requests, re, pandas as pd, urllib.request, os, json, pymongo, time

'''pn = page number, need to scrap'''
'''sc = region, 101-123, 201-225'''

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["real_estate_data"]
mycol = mydb["tokyo"]

url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ta=13&sc=13102&sngz=&po1=25&po2=99&pc=100&pn=1'
web_page = urllib.request.urlopen(url)
contents = web_page.read().decode(errors="replace")
web_page.close()
soup = BeautifulSoup(contents, 'html.parser')
total_page = int(soup.find_all('ol',{'class':'pagination-parts'})[0].find_all('li')[-1].get_text())
print(total_page)

house = soup.find_all('div', {'class': 'property-header'})
print(len(house))
total_list = []
data = {}
for n in range(total_page):
    page_num = n + 1
    if page_num % 30 == 0:
        time.sleep(20)
    url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ta=13&sc=13102&sngz=&po1=25&po2=99&pc=100&pn={page_num}'
    web_page = urllib.request.urlopen(url.format(page_num = page_num))
    contents = web_page.read().decode(errors="replace")
    web_page.close()
    soup = BeautifulSoup(contents, 'html.parser')

    #each house
    header = soup.find_all('div', {'class': 'property-header'})
    body = soup.find_all('div', {'class': 'property-body'})

    for i in range(len(header)):
        data["building_name"] = header[i].find_all("h2",{'class':"property_inner-title"})[0].get_text().strip()
        address = body[i].find_all("td",{"class": "detailbox-property-col"})[4].get_text().strip()
        data['address'] = address
        city, sub_city = re.split('都|道|府|县', address)
        data['city'] = city
        sub_city, machi = re.split('区|市|郡', sub_city)
        data["sub_city"] = sub_city
        machi = ''.join(['' if i.isdigit() else i for i in machi])
        data['machi'] = machi
        data["rent"] = body[i].find_all("div",{"class":"detailbox-property-point"})[0].get_text()[:-2]
        data["layout"] = body[i].find_all("td",
                                        {"class":"detailbox-property-col detailbox-property--col3"})[0].find_all("div")[0].get_text()
        data['area'] = body[i].find_all("td",
                                        {"class":"detailbox-property-col detailbox-property--col3"})[0].find_all("div")[1].get_text()[:-2]
        data["direction"] = body[i].find_all("td",
                                        {"class":"detailbox-property-col detailbox-property--col3"})[0].find_all("div")[2].get_text()
        data["type"] = body[i].find_all("td",
                                        {"class":"detailbox-property-col detailbox-property--col3"})[1].find_all("div")[0].get_text()
        data["years"] = body[i].find_all("td",
                                        {"class":"detailbox-property-col detailbox-property--col3"})[1].find_all("div")[1].get_text()[1:-1]
        transit = body[i].find_all("div",{"class":"detailnote-box"})[0]
        data["transit"] = [i.get_text() for i in transit.find_all("div")]
        #x = mycol.insert_one(data)
        #print(x.inserted_id)
        print(data.copy())
        total_list.append(data.copy())
    time.sleep(2)
    print(page_num)



final_list = [i for n, i in enumerate(total_list) if i not in total_list[n + 1:]]
print("done")
with open("data_file2.json", "w", encoding='utf-8') as f:
    json.dump(final_list, f, ensure_ascii=False)
