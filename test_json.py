import json, numpy as np

with open('data_file.json', encoding="utf8") as json_file:
    data = json.load(json_file)
print("the total data entries are:", len(data))

rent = [float(i["rent"]) for i in data]
size = [float(i["area"]) for i in data]
layout = set([i["layout"] for i in data])
building_type = set([i["type"] for i in data])
transit_time = [int(char) for i in data for n in i["transit"] for char in n if char.isdigit()]
layout_count = {}
for i in data:
    if i["layout"] not in layout_count:
        layout_count[i["layout"]] = 1
    else:
        layout_count[i["layout"]] += 1
sorted_x = sorted(layout_count.items(), key=lambda kv: kv[1], reverse=True)

years = [int(i["years"]) if i["years"] != "" else 0 for i in data]

direction_count = {}
machi_count = {}
for i in data:
    if i["direction"] not in direction_count:
        direction_count[i["direction"]] = 1
    else:
        direction_count[i["direction"]] += 1
for i in data:
    if i["machi"] not in machi_count:
        machi_count[i["machi"]] = 1
    else:
        machi_count[i["machi"]] += 1
direction = sorted(direction_count.items(), key=lambda kv: kv[1], reverse=True)
machi = sorted(machi_count.items(), key=lambda kv: kv[1], reverse=True)

print("the average rent is:",round(np.mean(rent), 2), "万日元")
print("the average size is:",round(np.mean(size), 2), "m2")
print("the types of layout are:",sorted_x[:5])
print("the types of directions are:", direction)
print("building types are:", building_type)
print("the average built years for buildings is:", round(np.mean(years), 0), "years")
print("the average time to walk to the closest transit station is:", round(np.mean(transit_time), 2), "min")
print("the most popular 町 are:",machi)
print()
print(data[0])

