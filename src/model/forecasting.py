import visibilityGraph as vg
import numpy as np

def zhang(timeseries):
    vgt = vg.visibilityGraph(timeseries)
    maxIndex = vgt.maxIndex
    diff = [vgt.tan(maxIndex[i], vgt.timeSerie[maxIndex[i]],
                    vgt.length-1, vgt.timeSerie[-1]) for i in range(len(maxIndex))]
    return vgt.timeSerie[-1]+ np.mean(np.array(diff))

def mao(timeseries):
    vgt = vg.visibilityGraph(timeseries)
    maxIndex = vgt.maxIndex
    diff = [vgt.tan(maxIndex[i], vgt.timeSerie[maxIndex[i]],
                    vgt.length-1, vgt.timeSerie[-1]) for i in range(len(maxIndex))]
    diff = [abs(maxIndex[i]-vgt.length + 1)/abs(maxIndex[i]-vgt.length)*diff[i] for i in range(len(diff))]
    return vgt.timeSerie[-1]+ np.mean(np.array(diff))

def zhan(timeseries):
    vgt = vg.visibilityGraph(timeseries)
    diff = [vgt.tan(i, vgt.timeSerie[i],
                    vgt.length-1, vgt.timeSerie[-1]) for i in range(vgt.length-1)]
    srw = vgt.SRW.copy()[:-1]
    srw = srw / np.sum(srw)
    diff = [srw[i]*diff[i] for i in range(vgt.length-1)]
    return vgt.timeSerie[-1]+ np.sum(np.array(diff))

def dataset(timeseries, start):
    x = timeseries[:-1]
    y = timeseries[1:]
    return [x[:i] for i in range(start+1, len(x)+1)], y[start:]
