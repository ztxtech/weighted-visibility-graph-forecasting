import math

import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签
color = [
    "#E64B35FF", "#4DBBD5FF", "#00A087FF", "#3C5488FF"]


def perror(yreal, yp):
    yp = np.array(yp)
    yreal = np.array(yreal)
    MAD = sum(np.abs(yp - yreal)) / len(yp)
    MAPE = 100 * sum(np.abs(yp - yreal) / yreal) / len(yp)
    SMAPE = 2 * 100 * sum(np.abs(yp - yreal) / np.abs((yreal + yp))) / len(yp)
    RMSE = math.sqrt(sum(np.abs(yp - yreal) * np.abs(yp - yreal)) / len(yp))
    NRMSE = 100 * math.sqrt(sum(np.abs(yp - yreal) * np.abs(yp - yreal)) / len(yp) / (max(yreal) - min(yreal)))
    error = [MAD, MAPE, SMAPE, RMSE, NRMSE]
    return error


df = pd.read_csv("./result/CCI.csv")
date = pd.read_csv("./data/CCI/CCI.CSV")['Date'].tolist()[7:]

y = df['y'].tolist()
zhan = df['zhan'].tolist()
zhang = df['zhang'].tolist()
mao = df['mao'].tolist()
arima = df['arima'].tolist()

zhanerror = []
zhangerror = []
maoerror = []
arimaerror = []
errordate = []

for i in range(2, len(y) + 1):
    errordate.append(date[i - 1])
    zhanerror.append(perror(y[:i], zhan[:i]))
    zhangerror.append(perror(y[:i], zhang[:i]))
    maoerror.append(perror(y[:i], mao[:i]))
    arimaerror.append(perror(y[:i], arima[:i]))

plt.figure(figsize=(20, 12), dpi=200)
plt.subplots_adjust(hspace=0.2, wspace=0.3)
error_name = ["MAE", "MAPE", "SMAPE", "RMSE", "NRMSE"]
index = 1
ci = 0
for i in range(5):
    plt.subplot(2, 3, index)
    index = index + 1
    plt.title(error_name[i] + " Error")
    plt.plot(range(len(errordate)), [j[i] for j in zhanerror], color=color[ci % (len(color))], lw=1.5,
             path_effects=[pe.Stroke(linewidth=3, foreground='black'), pe.Normal()])
    ci = ci + 1
    plt.plot(range(len(errordate)), [j[i] for j in zhangerror], color=color[ci % (len(color))], lw=1.5,
             path_effects=[pe.Stroke(linewidth=3, foreground='#676E73'), pe.Normal()])
    ci = ci + 1
    plt.plot(range(len(errordate)), [j[i] for j in maoerror], color=color[ci % (len(color))], lw=1.5,
             path_effects=[pe.Stroke(linewidth=3, foreground='#676E73'), pe.Normal()])
    ci = ci + 1
    plt.plot(range(len(errordate)), [j[i] for j in arimaerror], color=color[ci % (len(color))], lw=1.5,
             path_effects=[pe.Stroke(linewidth=3, foreground='#676E73'), pe.Normal()])
    ci = ci + 1
    plt.xticks(range(len(errordate))[::25], errordate[::25], rotation=60)
    plt.legend(["Proposed", "Zhang et al.", "Mao and Xiao", "ARIMA"])

plt.savefig("./fig/CCI_er.pdf")
plt.show()
