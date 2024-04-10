import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签


def perror(yreal, yp):
    yp = np.array(yp)
    yreal = np.array(yreal)
    MAD = sum(np.abs(yp - yreal)) / len(yp)
    MAPE = 100 * sum(np.abs(yp - yreal) / yreal) / len(yp)
    SMAPE = 2 * 100 * sum(np.abs(yp - yreal) / np.abs((yreal + yp))) / len(yp)
    RMSE = math.sqrt(sum(np.abs(yp - yreal) * np.abs(yp - yreal)) / len(yp))
    NRMSE = 100 * math.sqrt(sum(np.abs(yp - yreal) *
                                np.abs(yp - yreal)) / len(yp) / (max(yreal) - min(yreal)))
    error = [MAD, MAPE, SMAPE, RMSE, NRMSE]
    return error


df = pd.read_csv("./result/CCI.csv")
date = pd.read_csv("./data/CCI/CCI.CSV")['Date'].tolist()[7:]

plt.figure(figsize=(12, 5), dpi=200)
for i in df.columns[1:]:
    plt.plot(range(len(df)), df[i].tolist(), lw=(1 if i in ['y', 'zhan'] else 0.5))
plt.legend(['Actual', 'Proposed', 'Zhang et al.', 'Mao and Xiao', 'ARIMA'])
# plt.show()
plt.xticks(range(len(df))[::7], date[::7], rotation=60)
plt.savefig("./fig/CCI_compare.pdf")
plt.show()

c = df.columns
error = []
for i in range(2, len(c)):
    error.append(perror(df[c[1]], df[c[i]]))
error_df = pd.DataFrame(error, columns=['MAD', 'MAPE', 'SMAPE', 'RMSE', 'NRMSE'], index=c[2:])
error_df.to_csv("./error/CCI.csv")
