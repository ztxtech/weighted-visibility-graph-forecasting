import matplotlib.patheffects as pe
from matplotlib import pyplot as plt

from utils import data_loader

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签

filename = ['m1_yearly_dataset.tsf',
            'm1_quarterly_dataset.tsf',
            'm1_monthly_dataset.tsf',
            'm3_yearly_dataset.tsf',
            'm3_quarterly_dataset.tsf',
            'm3_monthly_dataset.tsf',
            'm3_other_dataset.tsf',
            ]

color = [
    "#1F77B4FF", "#FF7F0EFF", "#2CA02CFF", "#D62728FF", "#9467BDFF", "#8C564BFF",
    "#E377C2FF", "#7F7F7FFF", "#BCBD22FF", "#17BECFFF", "#AEC7E8FF", "#FFBB78FF",
    "#98DF8AFF", "#FF9896FF", "#C5B0D5FF", "#C49C94FF", "#F7B6D2FF", "#C7C7C7FF",
    "#DBDB8DFF", "#9EDAE5FF"]

color = [
    "#E64B35FF", "#4DBBD5FF", "#00A087FF", "#3C5488FF", "#F39B7FFF", "#8491B4FF",
    "#91D1C2FF", "#DC0000FF", "#7E6148FF", "#B09C85FF"]

plt.figure(figsize=(100 / 4, 140 / 4))
plt.dpi = 200
index = 1
for idx1, file in enumerate(filename):

    datasetlist = data_loader.get_dataset("./data/tsf/" + file)
    for idx2, data in enumerate(datasetlist):
        if idx2 == 4:
            break
        plt.subplot(len(filename), 4, index)
        yp = []
        xlist = data[0][0]
        y = data[1]
        plt.title(file.replace("_dataset.tsf", "").replace("_", " ").title() + " Time Series " + str(idx2 + 1))
        plt.plot(range(len(xlist)), xlist, color=color[index % len(color)], lw=2,
                 path_effects=[pe.Stroke(linewidth=4, foreground='#CCCCCC'), pe.Normal()])
        plt.xticks(size=12)
        index = index + 1
plt.savefig("./fig/m1m3.pdf")
