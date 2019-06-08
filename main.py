from bs4 import BeautifulSoup
import requests, re, pandas as pd, urllib.request, os

url = 'https://suumo.jp/chintai/tokyo/city/'
web_page = urllib.request.urlopen(url)
contents = web_page.read().decode(errors="replace")
web_page.close()

soup = BeautifulSoup(contents, 'html.parser')

all_link = [os.path.basename(i['href'][:-1])
            for body in soup.find_all('dd',{'class':'itemlinebox-body itemlinkline-body'}) for i in body.find_all('a')]
all_link = [i for i in all_link if 'sc_' in i]
all_link = [url.replace("city/","") + i + '/'for i in all_link]

new_url = all_link[0]

web_page = urllib.request.urlopen(new_url)
contents = web_page.read().decode(errors="replace")
web_page.close()
soup = BeautifulSoup(contents, 'html.parser')

building = [i for i in soup.find_all('div',{'class':'cassetteitem'})]

#building name
print(building[0].find_all('div',{'class':'cassetteitem_content-title'})[0].get_text())

#address name
address = building[0].find_all('li',{'class':'cassetteitem_detail-col1'})[0].get_text()
print(address)

#city name
city, sub_city = re.split('都|道|府|县',address)
print(city)

