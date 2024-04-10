import os

import autots.evaluator.metrics
import numpy as np
import pandas as pd

filelist = os.listdir("./data/tsf")
reslist = os.listdir("./result")

AVG_list = []

for file in filelist:

    res = []
    for i in reslist:
        if i.find(file) != -1:
            res.append(i)

    MAE_list = []
    SMAPE_list = []

    for r in res:
        df = pd.read_csv("./result/" + r)
        MAE_list.append(autots.evaluator.metrics.mean_absolute_error(df['y'].to_numpy(), df['yp'].to_numpy()))
        SMAPE_list.append(
            autots.evaluator.metrics.symmetric_mean_absolute_percentage_error(df['y'].to_numpy(), df['yp'].to_numpy()))

    error = pd.DataFrame(np.array([MAE_list, SMAPE_list]).T, columns=['MAE', "SMAPE"], index=res)

    AVG_list.append([sum(MAE_list) / len(MAE_list), sum(SMAPE_list) / len(SMAPE_list)])
    error.to_csv("./error/" + file + "_error.csv")

error_avg = pd.DataFrame(np.array(AVG_list), columns=['MAE', 'SMAPE'], index=filelist)
error_avg.to_csv("./error/all_error_avg.csv")
