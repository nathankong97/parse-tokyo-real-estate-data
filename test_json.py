import json, numpy as np, matplotlib.pyplot as plt,re
from scipy import stats
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

#read and load the json data
with open('data_file.json', encoding="utf8") as json_file:
    data = json.load(json_file)

#basic informative statistical data
print("the total data entries are:", len(data))
rent = [float(i["rent"]) for i in data]
size = [float(i["area"]) for i in data]
layout = set([i["layout"] for i in data])
building_type = set([i["type"] for i in data])
transit_time = [int(re.findall("\d+", n)[0]) for i in data for n in i["transit"] if re.findall("\d+", n) != []]
years = [int(i["years"]) if i["years"] != "" else 0 for i in data]

#store the value as dict
layout_count = {}
layout_rent = {}
for i in data:
    if i["layout"] not in layout_count:
        layout_count[i["layout"]] = 1
    else:
        layout_count[i["layout"]] += 1
    if i["layout"] not in layout_rent:
        layout_rent[i["layout"]] = [float(i["rent"])]
    else:
        layout_rent[i["layout"]].append(float(i["rent"]))
sorted_x = sorted(layout_count.items(), key=lambda kv: kv[1], reverse=True)
avg_values = [round(np.mean(i),2) for i in layout_rent.values()]
avg_rent_by_layout = dict(zip(layout_rent.keys(), avg_values))
sort_avg_rent_by_layout = sorted(avg_rent_by_layout.items(), key=lambda kv: kv[1], reverse=True)


direction_count = {}
direction_rent = {}
machi_count = {}
for i in data:
    if i["direction"] not in direction_count:
        direction_count[i["direction"]] = 1
    else:
        direction_count[i["direction"]] += 1
    if i["direction"] not in direction_rent:
        direction_rent[i["direction"]] = [float(i["rent"])]
    else:
        direction_rent[i["direction"]].append(float(i["rent"]))
avg_values = [round(np.mean(i),2) for i in direction_rent.values()]
avg_rent_by_direction = dict(zip(direction_rent.keys(), avg_values))
sort_avg_rent_by_direction = sorted(avg_rent_by_direction.items(), key=lambda kv: kv[1], reverse=True)

machi_rent = {}
for i in data:
    if i["machi"] not in machi_count:
        machi_count[i["machi"]] = 1
    else:
        machi_count[i["machi"]] += 1
    if i["machi"] not in machi_rent:
        machi_rent[i["machi"]] = [float(i["rent"])]
    else:
        machi_rent[i["machi"]].append(float(i["rent"]))
avg_values = [round(np.mean(i),2) for i in machi_rent.values()]
avg_rent_by_machi = dict(zip(machi_rent.keys(), avg_values))
sort_avg_rent_by_machi = sorted(avg_rent_by_machi.items(), key=lambda kv: kv[1], reverse=True)
direction = sorted(direction_count.items(), key=lambda kv: kv[1], reverse=True)
machi = sorted(machi_count.items(), key=lambda kv: kv[1], reverse=True)

type_rent = {}
type_count = {}
for i in data:
    if i["type"] not in type_rent:
        type_rent[i["type"]] = [float(i["rent"])]
    else:
        type_rent[i["type"]].append(float(i["rent"]))
    if i["type"] not in type_count:
        type_count[i["type"]] = 1
    else:
        type_count[i["type"]] += 1
avg_values = [round(np.mean(i),2) for i in type_rent.values()]
avg_rent_by_type = dict(zip(type_rent.keys(), avg_values))
sort_avg_rent_by_type = sorted(avg_rent_by_type.items(), key=lambda kv: kv[1], reverse=True)

#transit information
transit_num = [len([int(re.findall("\d+",n)[0]) for n in i["transit"] if re.findall("\d+",n) != []]) for i in data]



#output
#print(transit_num)
print(direction_rent)
print("the average rent by building types are:",sort_avg_rent_by_type)
print("the 5 most expensive 町 are:",sort_avg_rent_by_machi[::-1][:5])
print("the 5 cheapest 町 are:",sort_avg_rent_by_machi[:5])
print("the average rent by direction are:", sort_avg_rent_by_direction)
print("the 5 cheapest layout are:",sort_avg_rent_by_layout[::-1][:5])
print("the 5 most expensive layout are:",sort_avg_rent_by_layout[:5])
print("the coorelation coefficient between rent and size is:", round(np.corrcoef(rent, size)[0][1], 4))
print("the coorelation coefficient between rent and built year is:", round(np.corrcoef(rent, years)[0][1], 4))
print("the coorelation coefficient between built years and size year is:", round(np.corrcoef(years, size)[0][1], 4))
print("the average rent is:",round(np.mean(rent), 2), "万日元")
print("the average size is:",round(np.mean(size), 2), "m2")
print("the types of layout are:",sorted_x[:5])
print("the types of directions are:", direction)
print("building types are:", building_type)
print("the average built years for buildings is:", round(np.mean(years), 0), "years")
print("the average time to walk to the closest transit station is:", round(np.mean(transit_time), 2), "min")
print("the most popular 町 are:",machi[:5])
print()
#print(data[0])


labels, direction_data = [*zip(*direction_rent.items())]
plt.boxplot(direction_data)
plt.xticks(range(1, len(labels) + 1), labels)
plt.show()

plt.xlim(0,140)
plt.ylim(0,2400)
#plt.rcParams["figure.figsize"] = (15,7)
plt.title("Tokyo Chiyoda Housing Rent Price")
plt.xlabel("Rent (thousand yen)")
plt.ylabel("Quantity")
plt.hist(rent, bins=60)
plt.vlines(np.mean(rent), 0, 2400, color='red', label='average_price', linewidth=1.5, linestyle='--')
plt.vlines(np.median(rent), 0, 2400, color='red',label='median_price', linewidth=1.5)
plt.legend()
plt.show()

x = np.asarray(rent)
y = np.asarray(size)
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
line = slope * x + intercept
plt.plot(x, line, 'r', label='y={:.2f}x+{:.2f}'.format(slope,intercept), c = 'blue', linewidth = 1)
plt.scatter(x, y, c = "red", alpha=0.3, s = 50)
plt.title('Scatter Correlation between Rent and Size')
plt.xlabel("Rent (ten thousand yen)")
plt.ylabel('Size (m2)')
plt.show()

x = np.asarray(rent)
y = np.asarray(years)
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
line = slope * x + intercept
plt.plot(x, line, 'r', label='y={:.2f}x+{:.2f}'.format(slope,intercept), c = 'black', linewidth = 1)
plt.scatter(x, y, c = "green", alpha=0.3, s = 50)
plt.title('Scatter Correlation between Rent and Built Years')
plt.xlabel("Rent (ten thousand yen)")
plt.ylabel('Year(s)')
plt.show()

x = np.asarray(years)
y = np.asarray(size)
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
line = slope * x + intercept
plt.plot(x, line, 'r', label='y={:.2f}x+{:.2f}'.format(slope,intercept), c = 'pink', linewidth = 1)
plt.scatter(x, y, c = "grey", alpha=0.3, s = 50)
plt.title('Scatter Correlation between built years and Size')
plt.xlabel("Years)")
plt.ylabel('Size (m2)')
plt.show()