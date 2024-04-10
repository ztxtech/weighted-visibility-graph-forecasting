import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签

"""
    构造降序排序矩阵
"""


def rank_matrix(matrix):
    cnum = matrix.shape[1]
    rnum = matrix.shape[0]
    ## 升序排序索引
    sorts = np.argsort(matrix)
    for i in range(rnum):
        k = 1
        n = 0
        flag = False
        nsum = 0
        for j in range(cnum):
            n = n + 1
            ## 相同排名评分序值
            if j < 3 and matrix[i, sorts[i, j]] == matrix[i, sorts[i, j + 1]]:
                flag = True;
                k = k + 1;
                nsum += j + 1;
            elif (j == 3 or (j < 3 and matrix[i, sorts[i, j]] != matrix[i, sorts[i, j + 1]])) and flag:
                nsum += j + 1
                flag = False;
                for q in range(k):
                    matrix[i, sorts[i, j - k + q + 1]] = nsum / k
                k = 1
                flag = False
                nsum = 0
            else:
                matrix[i, sorts[i, j]] = j + 1
                continue
    return matrix


"""
    Friedman检验
    参数：数据集个数n, 算法种数k, 排序矩阵rank_matrix(k x n)
    函数返回检验结果（对应于排序矩阵列顺序的一维数组）
"""


def friedman(n, k, rank_matrix):
    # 计算每一列的排序和
    sumr = sum(list(map(lambda x: np.mean(x) ** 2, rank_matrix.T)))
    result = 12 * n / (k * (k + 1)) * (sumr - k * (k + 1) ** 2 / 4)
    result = (n - 1) * result / (n * (k - 1) - result)
    return result


"""
    Nemenyi检验
    参数：数据集个数n, 算法种数k, 排序矩阵rank_matrix(k x n)
    函数返回CD值
    R: qtukey(1- alpha, k, Inf)/sqrt(2)
"""


def nemenyi(n, k, q):
    return q * (np.sqrt(k * (k + 1) / (6 * n)))


# color = ['#BC3C29FF','#0072B5FF','#E18727FF','#20854EFF','#7876B1FF','#6F99ADFF','#FFDC91FF','#EE4C97FF']
cstr = "#E64B35FF#4DBBD5FF#00A087FF#3C5488FF#F39B7FFF#8491B4FF#91D1C2FF#DC0000FF#7E6148FF#B09C85FF"
color = []
for i in cstr.split("#"):
    if i != "":
        color.append("#" + i)

df = pd.read_csv("./error/mo_mae.csv")
methods = df.columns[1:].tolist()
dataname = df['Dataset'].tolist()

matrix = np.array([df[i].tolist() for i in methods])
matrix_r = rank_matrix(matrix.T)
n = len(dataname)
k = len(methods)
Friedman = friedman(n, k, matrix_r)
CD = nemenyi(n, k, 3.312739)
##画CD图
rank_x = list(map(lambda x: np.mean(x), matrix))
name_y = methods
min_ = [x for x in rank_x - CD / 2]
max_ = [x for x in rank_x + CD / 2]

plt.figure(figsize=(10 * 1.5, 7.5 * 1.5), dpi=300)
plt.subplots_adjust(wspace=0.5)

plt.subplot(1, 2, 1)
plt.title("MAE ERROR")
for i in range(len(max_)):
    plt.vlines(max_[i], 0, name_y[i], color=color[i % len(color)], linestyles="--", lw=0.8)
for i in range(len(max_)):
    plt.hlines(name_y[i], min_[i], max_[i], color=color[i % len(color)], lw=3,
               path_effects=[pe.Stroke(linewidth=3, foreground='#7F7F7F'), pe.Normal()])
plt.scatter(rank_x, name_y, c='#1B19197F', s=50, edgecolors="#7F7F7F")

df = pd.read_csv("./error/mo_smape.csv")
methods = df.columns[1:].tolist()
dataname = df['Dataset'].tolist()

matrix = np.array([df[i].tolist() for i in methods])
matrix_r = rank_matrix(matrix.T)
n = len(dataname)
k = len(methods)
Friedman = friedman(n, k, matrix_r)
CD = nemenyi(n, k, 3.312739)
##画CD图
rank_x = list(map(lambda x: np.mean(x), matrix))
name_y = methods
min_ = [x for x in rank_x - CD / 2]
max_ = [x for x in rank_x + CD / 2]

plt.subplot(1, 2, 2)
plt.title("SMAPE ERROR")

for i in range(len(max_)):
    plt.vlines(max_[i], 0, name_y[i], color=color[i % len(color)], linestyles="--", lw=0.8)
for i in range(len(max_)):
    plt.hlines(name_y[i], min_[i], max_[i], color=color[i % len(color)], lw=3,
               path_effects=[pe.Stroke(linewidth=3, foreground='#7F7F7F'), pe.Normal()])

plt.scatter(rank_x, name_y, c='#1B19197F', s=50, edgecolors="#7F7F7F")

plt.savefig("./fig/m1m3cp.pdf")
plt.show()
