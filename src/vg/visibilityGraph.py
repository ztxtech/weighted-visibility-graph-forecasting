import numpy as np

class visibilityGraph:

    def tan(self, x_1, y_1, x_2, y_2):
        return (y_2 - y_1) / (x_2 - x_1)

    def __init__(self, timeSerie):
        self.timeSerie = timeSerie
        self.length = len(timeSerie)
        self.lowerBound = int(min(timeSerie)) - int(np.std(self.timeSerie))
        self.setVisibilityMatrix()
        self.setAdjacencyMatrix()
        self.setDegreeVector()
        self.setEdgeNumber()
        self.setPiMatrix()
        self.setSRW()

    def setVisibilityMatrix(self):
        temp = np.zeros((self.length, self.length))
        for i in range(self.length):
            for j in range(i+1,self.length):
                    temp[i,j]=self.tan(i,self.timeSerie[i],j,self.timeSerie[j])
        temp=temp+temp.T
        self.visibilityMatrix = temp

    def setAdjacencyMatrix(self):
        result = np.zeros((self.length, self.length))
        for i in range(self.length):
            for j in range(i+1,self.length):
                if max(self.visibilityMatrix[i,i+1:j+1])==self.visibilityMatrix[i,j]:
                    result[i,j]=1
        result=result+result.T
        self.adjacencyMatrix = result

    def setDegreeVector(self):
        self.degreeVector = np.sum(self.adjacencyMatrix, axis=1)

    def setEdgeNumber(self):
        self.edgeNumber = np.sum(self.degreeVector)

    def setPiMatrix(self):
        result = self.adjacencyMatrix.copy()
        for i in range(self.length):
            k = self.degreeVector[i]
            for j in range(self.length):
                result[i, j] = result[i, j] / k
        self.pMatrix = result

    def setPVectorList(self):
        self.pVectorList = []
        for i in range(self.length):
            px = np.zeros((self.length, 1))
            px[i, 0] = 1
            self.pVectorList.append(px)

    def setSRW(self, time=500):
        self.setPVectorList()
        self.SRW = np.zeros((self.length, 1))
        t = 0
        LRW_temp = np.zeros((self.length, 1))
        while True and t<time:
            t = t + 1
            #p
            for i in range(self.length):
                self.pVectorList[i] = np.matmul((self.pMatrix.T), self.pVectorList[i])
            #LRW
            LRW = np.zeros((self.length, 1))
            for i in range(self.length):
                LRW[i] = self.degreeVector[i] / self.edgeNumber * self.pVectorList[i][-1] \
                                + self.degreeVector[-1] / self.edgeNumber * self.pVectorList[-1][i]
            LRW = np.around(LRW, 6)
            if (LRW == LRW_temp).all():
                break
            else:
                LRW_temp = LRW.copy()
            #SRW
            self.SRW = self.SRW + LRW
        self.time = t
        self.SRW = self.SRW.reshape(-1)
        self.setMaxIndex()

    def setMaxIndex(self):
        index = np.array(np.where(self.SRW[:-1] == np.max(self.SRW[:-1])))
        self.maxIndex = index.reshape(-1).tolist()

    def generateDotList(self):
        dotlist = []
        for idx, v in enumerate(self.timeSerie):
            dotlist.append((idx+1, v))
        return dotlist

    def generateEdgeList(self):
        edgeList = []
        for i in range(self.length-1):
            curEdgeList = []
            for j in range(i, self.length):
                if self.adjacencyMatrix[i][j]==1.0:
                    curEdgeList.append([(i+1, self.timeSerie[i]),(j+1, self.timeSerie[j])])
            edgeList.append(curEdgeList)
        return edgeList

    def generateGraphEdgeList(self):
        edgeListS = []
        edgeListC = []
        for i in range(self.length-1):
            edgeListS.append((i+1, i+2))
        for i in range(self.length-1):
            for j in range(i+2, self.length):
                if self.adjacencyMatrix[i][j]==1.0:
                    edgeListC.append((i+1,j+1))
        return edgeListS, edgeListC

    def generateTexCode(self):
        code = []
        code.append("\\begin{figure}[htbp]")
        code.append("	\\centering")
        code.append("	")
        code.append("	\\begin{tikzpicture}[scale = 0.8]")
        code.append("        \\begin{axis}[")
        code.append("        axis lines=left,")
        code.append("        xlabel = $t$,")
        code.append("        ylabel = $y$,")
        code.append("        ybar=-0.5cm,")
        code.append("        bar width=0.5cm,")
        code.append("        ymin=%s,"%(str(self.lowerBound)))
        code.append("        width=15cm, %x轴长度")
        code.append("        height=8cm, %y轴长度")
        code.append("        enlarge x limits=.1,")
        code.append("        ]")
        dotlist = self.generateDotList()
        s = ""
        for i in dotlist:
            s = s + str(i)+" "
        code.append("        \\addplot[draw=black,fill=blue!70] coordinates {%s};"%(s))
        code.append("        \\addplot[sharp plot, thick,draw=red!100] coordinates {")
        edgelist = self.generateEdgeList()
        for dotEgelist in edgelist:
            edgeEdgeListStr = ""
            for edge in dotEgelist:
                for dot in edge:
                    edgeEdgeListStr =  edgeEdgeListStr + str(dot) + " "
            code.append("            %s"%(edgeEdgeListStr))
        code.append("            };")
        code.append("        \\end{axis}")
        code.append("	\\end{tikzpicture}")
        code.append("")
        code.append("	\\begin{tikzpicture}[scale = 0.8]")
        code.append("	\\centering")
        code.append("	\\tikzstyle{every node}=[draw,shape=circle]")
        edgelistS, edgelistC = self.generateGraphEdgeList()
        code.append("	\\draw[thick, draw=blue!50] (%s,0) node[circle,fill,inner sep=3pt,label=below: $t_{%s}$ ](%s){} -- (%s,0) node[circle,fill,inner sep=3pt,label=below: $t_{%s}$ ](%s){};"%(edgelistS[0][0], edgelistS[0][0], edgelistS[0][0], edgelistS[0][1], edgelistS[0][1], edgelistS[0][1]))
        for i in range(1, len(edgelistS)):
            code.append("	\\draw[thick, draw=blue!50](%s) -- (%s,0) node[circle,fill,inner sep=3pt,label=below: $t_{%s}$ ](%s){};"%(edgelistS[i][0], edgelistS[i][1], edgelistS[i][1], edgelistS[i][1]))
        for i in edgelistC:
            code.append("	\\draw (%s) to[out=70,in=110] (%s,0);"%(i[0], i[1]))
        code.append("\\end{tikzpicture}")
        code.append("\\caption{caption}")
        code.append("\\end{figure}")
        return code


vg = visibilityGraph([1,2,3])