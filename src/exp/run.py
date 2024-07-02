import os

import numpy as np
import pandas as pd

import fs
from utils import data_loader

filename = os.listdir("./data/tsf")

for file in filename:

    datasetlist = data_loader.get_dataset("./data/tsf/" + file)

    for idx, data in enumerate(datasetlist):
        yp = []
        xlist = data[0]
        y = data[1]
        print(len(xlist[0]))
        for x in xlist:
            yp.append(fs.zhan(x[-200:]))
        df_temp = pd.DataFrame(np.array([y, yp]).T, columns=['y', 'yp'])
        df_temp.to_csv("./result/" + file + "_T" + str(idx) + ".csv")
        print(file + "_T" + str(idx))
