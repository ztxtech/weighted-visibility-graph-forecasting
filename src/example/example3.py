import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import VG.visibilityGraph as vg

plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签


def tan(x_1, y_1, x_2, y_2):
    return (y_2 - y_1) / (x_2 - x_1)


def predicted(x_1, y_1, x_2, y_2, x_3):
    t = tan(x_1, y_1, x_2, y_2)
    return y_2 + t * (x_3 - x_2)


def plotline(p1, p2, color1="#F28749", color2="#7F7F7F"):
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color1, lw=2)
    plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], color=color2, edgecolor='#1B1919FF')


color = [
    "#E64B35FF", "#4DBBD5FF", "#00A087FF", "#3C5488FF", "#F39B7FFF", "#8491B4FF",
    "#91D1C2FF", "#DC0000FF", "#7E6148FF", "#B09C85FF"]

df = pd.read_csv("./data/CCI/CCI.CSV")[36:47]
date = df['Date'].tolist()
data = df["Value"].tolist()
target = data[-1]
data = data[:-1]

a = vg.visibilityGraph(data)
print(a.SRW[:-1])
print(a.SRW[:-1] / np.sum(a.SRW[:-1]))
b = a.SRW.tolist()

plt.figure(figsize=(10, 5), dpi=300)
plt.title("A fragment of the CCI dataset")
plt.xticks(range(0, len(data) + 1), date)
for i in range(len(data)):
    plt.bar([i], [data[i]], width=0.3, color=color[i % len(color)], edgecolor='#1B1919FF')

plt.ylim(5050, 5300)
i = a.maxIndex

for i in range(a.length - 1):
    plotline([i, data[i]], [len(data), predicted(i, data[i], len(data) - 1, data[len(data) - 1], len(data))],
             color1=color[i % len(color)])
    plotline([len(data) - 1, data[len(data) - 1]],
             [len(data), predicted(i, data[i], len(data) - 1, data[len(data) - 1], len(data))],
             color1=color[(len(data) - 1) % len(color)])
    print(predicted(i, data[i], len(data) - 1, data[len(data) - 1], len(data)), end=" ")
plt.axvline(x=len(data), ls="--", c="#012030", lw=1.5)

plt.savefig("./fig/CCI_ex.pdf")
plt.show()
#
# for i in a.generateTexCode():
#     print(i)


import fs.forecasting as fs

print(target)
print(fs.zhang(data))
print(fs.zhan(data))
print(fs.mao(data))

# for i in a.generateTexCode():
#     print(i)
