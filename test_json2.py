import json, numpy as np, matplotlib.pyplot as plt,re
from scipy import stats
from pylab import *
from collections import Counter
mpl.rcParams['font.sans-serif'] = ['SimHei']

#read and load the json data
with open('data_file2.json', encoding="utf8") as json_file:
    data = json.load(json_file)

print("the total data entries are:", len(data))

rent = [float(i["rent"]) for i in data]
size = [float(i["area"]) for i in data]

print(np.mean(rent))
print(np.mean(size))