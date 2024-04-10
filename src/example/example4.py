import pandas as pd

import VG.visibilityGraph_torch as vg
import fs.forecasting as fs

df = pd.read_csv("./data/CCI/CCI.CSV")[36:47]
data = df["Value"].tolist()
target = data[-1]
x = data[:-1]

g = vg.visibilityGraph(x)

zhan = fs.zhan(x)
zhang = fs.zhang(x)
mao = fs.mao(x)

f = [x[-1] + g.tan(idx, i, len(x) - 1, x[-1]) for idx, i in enumerate(x[:-1])]

print(target, zhan, zhang, mao)
