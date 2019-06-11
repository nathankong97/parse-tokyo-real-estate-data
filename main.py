from bs4 import BeautifulSoup
from datetime import datetime
import requests, re, pandas as pd, urllib.request, os, json, pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["real_estate_data"]
mycol = mydb["tokyo"]

'''data = {"building_name": "",
        "address": "",
        "city": "",
        "sub_city": "",
        "machi": "",
        "transit": "",
        "year" : "",
        "level": "",
        "rent": "",
        "type": "",
        "area": ""
        }'''
def main():
    data = {}
    url = 'https://suumo.jp/chintai/tokyo/sc_chiyoda/pnz11.html'
    web_page = urllib.request.urlopen(url)
    contents = web_page.read().decode(errors="replace")
    web_page.close()
    soup = BeautifulSoup(contents, 'html.parser')
    total_page = int(soup.find_all('ol',{'class':'pagination-parts'})[0].find_all('li')[-1].get_text())
    print(total_page)
    count1 = count2 = count3 = 0
    with open('data_file.json', 'a', encoding='utf-8') as f:
        ##Open the json file, and start to loop each page
        total_list = []
        for i in range(total_page):
            page_list = []
            num = i + 1
            url = 'https://suumo.jp/chintai/tokyo/sc_chiyoda/pnz1{num}.html'
            web_page = urllib.request.urlopen(url.format(num = num))
            contents = web_page.read().decode(errors="replace")
            web_page.close()
            soup = BeautifulSoup(contents, 'html.parser')
            #all_link = [os.path.basename(i['href'][:-1])
            #            for body in soup.find_all('dd',{'class':'itemlinebox-body itemlinkline-body'}) for i in body.find_all('a')]
            #all_link = [i for i in all_link if 'sc_' in i]
            #all_link = [url.replace("city/","") + i + '/'for i in all_link]
            #new_url = all_link[0]
            count1 += 1
            ##inside of the page, loop each of the building
            for building in soup.find_all('div',{'class':'cassetteitem'}):
                building_list = []
                data['building_name'] = building.find_all('div',{'class':'cassetteitem_content-title'})[0].get_text()  #building name
                address = building.find_all('li',{'class':'cassetteitem_detail-col1'})[0].get_text()
                data['address'] = address  #address
                city, sub_city = re.split('都|道|府|县', address)
                data['city'] = city  #city
                sub_city, machi = re.split('区|市|郡', sub_city)
                data["sub_city"] = sub_city  #sub_city
                machi = ''.join(['' if i.isdigit() else i for i in machi])
                data['machi'] = machi  #machi
                transport = [i.get_text() for i in
                             building.find_all('li', {'class': 'cassetteitem_detail-col2'})[0].find_all('div')]
                data['transit'] = transport  #transit
                year = building.find_all('li', {'class': 'cassetteitem_detail-col3'})[0].find_all('div')[0].get_text()
                try:
                    if re.findall('\d', year)[0] != '':
                        year = int(datetime.now().year) - int(re.findall('\d', year)[0])
                        data['year'] = year  #year
                except:
                    data['year'] = int(datetime.now().year)  #year this year
                    pass
                count2 += 1
                #inside of the building, loop houses or apartment
                for house in building.find_all('div',{'class':'cassetteitem-item'})[0].find_all('tr')[1:]:
                    data = data
                    try:
                        level = int(''.join([i for i in house.find_all('td')[2].get_text() if i.isdigit()]))
                        data['level'] = level  #floor level
                    except:
                        data['level'] = ""
                        pass
                    rent = float(''.join([i for i in
                                          house.find_all('td')[3].find_all('span', {
                                              'class': 'cassetteitem_price cassetteitem_price--rent'})[0].get_text()])[:-2])
                    data['rent'] = rent  #housing rent
                    house_type = house.find_all('td')[5].find_all('li')[0].get_text()
                    data['type'] = house_type  #housing type
                    area = float(house.find_all('td')[5].find_all('li')[1].get_text()[:-2])
                    data['area'] = area  #housing area
                    count3 += 1
                    print(count1, count2, count3)
                    building_list.append(data)
                page_list = page_list + building_list
            total_list = total_list + page_list
        json.dump(total_list, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
    print()
    print("done")


