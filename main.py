from bs4 import BeautifulSoup
from datetime import datetime
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

sub_city, machi = re.split('区|市|郡',sub_city)
print(sub_city)

machi = ''.join(['' if i.isdigit() else i for i in machi])
print(machi)

transport = [i.get_text() for i in building[0].find_all('li',{'class':'cassetteitem_detail-col2'})[0].find_all('div')]
print(transport)

year = building[0].find_all('li',{'class':'cassetteitem_detail-col3'})[0].find_all('div')[0].get_text()
if re.findall('\d', year)[0] != '':
    print(int(datetime.now().year) - int(re.findall('\d', year)[0]))
else:
    print(int(datetime.now().year))

house = building[0].find_all('div',{'class':'cassetteitem-item'})[0].find_all('tr')[1]
level = int(''.join([i for i in house.find_all('td')[2].get_text() if i.isdigit()]))
print(level)

rent = float(''.join([i for i in
        house.find_all('td')[3].find_all('span',{'class':'cassetteitem_price cassetteitem_price--rent'})[0].get_text()])[:-2])
print(rent)

house_type = house.find_all('td')[5].find_all('li')[0].get_text()
print(house_type)

area = float(house.find_all('td')[5].find_all('li')[1].get_text()[:-2])
print(area)