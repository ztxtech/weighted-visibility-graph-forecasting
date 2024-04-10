import pandas as pd
import torch
from matplotlib import pyplot as plt

import VG.visibilityGraph_torch as vg

plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签


def tan(x_1, y_1, x_2, y_2):
    return (y_2 - y_1) / (x_2 - x_1)


def predicted(x_1, y_1, x_2, y_2, x_3):
    t = tan(x_1, y_1, x_2, y_2)
    return y_2 + t * (x_3 - x_2)


def plotline(p1, p2, color1="#F28749", color2="#7F7F7F"):
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color1)
    plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], color=color2, edgecolor='#1B1919FF')


color = [
    "#E64B35FF", "#4DBBD5FF", "#00A087FF", "#3C5488FF", "#F39B7FFF", "#8491B4FF",
    "#91D1C2FF", "#DC0000FF", "#7E6148FF", "#B09C85FF"]

df = pd.read_csv("./data/CCI/CCI.CSV")[37:47]
data = df["Value"].tolist()
target = data[-1]
x = data[:-1]

data = [10, 90, 30, 50, 20, 40, 60, 50, 30, 40]
a = vg.visibilityGraph(data)
print(a.SRW[:-1] / torch.sum(a.SRW[:-1]))

plt.figure(figsize=(10, 5), dpi=300)
plt.title("The way previous studies predicted")
plt.xticks(range(0, len(data) + 1), range(1, len(data) + 2))
for i in range(len(data)):
    plt.bar([i], [data[i]], color=color[i % len(color)] if i == a.maxIndex.item() or i == (len(data) - 1) else "grey",
            width=0.3, edgecolor='#1B1919FF')

plt.ylim()
i = a.maxIndex.item()
plotline([i, data[i]], [len(data), predicted(i, data[i], len(data) - 1, data[len(data) - 1], len(data))],
         color1=color[(i) % (len(color))])
plotline([len(data) - 1, data[len(data) - 1]],
         [len(data), predicted(i, data[i], len(data) - 1, data[len(data) - 1], len(data))],
         color1=color[(len(data) - 1) % (len(color))])
print(predicted(i, data[i], len(data) - 1, data[len(data) - 1], len(data)), end=" ")
plt.axvline(x=len(data), ls="--", c="#012030", lw=1.5)

plt.savefig("./fig/previous.pdf")
plt.show()

for i in a.generateTexCode():
    print(i)

import fs.forecasting as fs

print(fs.zhang(data))
print(fs.zhan(data))
