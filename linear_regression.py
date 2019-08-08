import os
import pandas as pd
import matplotlib.pyplot as plt

x_result = []
y_result = []

def importData(x, y, z): 
    dir = os.path.dirname(__file__)
    path = str(dir + "/" + x)
    data = pd.read_csv(path)
    jList = list(data[y])
    kList = list(data[z])
    return jList, kList
    
def runErrorAnalysis(bValue, mValue, j, k): 
    totalError = 0
    for x in range(len(j)): 
        totalError = totalError + (k[x] - (mValue * j[x] + bValue)) ** 2
    return totalError

def runGradientDescent(jRate, kRate, iter, initB, initM, j, k): 
    currentB = initB
    currentM = initM
    
    for x in range(iter): 
        currentB, currentM = runGradientDescentStepper(currentB, currentM, jRate, kRate, j, k)
        printIter = str(x)
        printB = str(format(currentB, ".10f"))
        printM = str(format(currentM, ".10f"))
        printError = str(runErrorAnalysis(currentB, currentM, j, k))
        print("iterations = " + printIter + ", B = " + printB + ", M = " + printM + ", error = " + printError)
    return currentB, currentM
    
def runGradientDescentStepper(currentB, currentM, jRate, kRate, a, n): 
    bChange = 0
    mChange = 0
    
    N = float(len(a))
    
    for i in range(len(a)): 
        bChange = bChange - 2 / N * (n[i] - (currentM * a[i] + currentB))
        mChange = mChange - 2 / N * a[i] * (n[i] - (currentM * a[i] + currentB))
    newB = currentB - jRate * bChange
    newM = currentM - kRate * mChange
    
    return newB, newM

def runLinearReg(jList, kList, jLearningRate, kLearningRate, iterations, initialB, initialM): 
    
    
    b, m = runGradientDescent(jLearningRate, kLearningRate, iterations, initialB, initialM, jList, kList)
    printIter = str(iterations)
    printB = str(format(b, ".10f"))
    printM = str(format(m, ".10f"))
    printError = str(runErrorAnalysis(b, m, jList, kList))
    print("\n\n\n\n\n\n\n\n\niterations = " + printIter + ", B = " + printB + ", M = " + printM + ", error = " + printError)
    return b, m


fileName = "goog.csv"
xColumnName = "time"
yColumnName = "value"
jLearningRate = 0.01
kLearningRate = 0.000001
iterations = 10000
initialB = 0
initialM = 0
graphDomainMin = 0
graphDomainMax= 1000

j, k = importData(fileName, xColumnName, yColumnName)
b, m = runLinearReg(j, k, jLearningRate, kLearningRate, iterations, initialB, initialM)
plt.plot(j, k, "o", markersize = 2)
for i in range(graphDomainMin, graphDomainMax): 
    x_result.append(i)
    y_result.append(i*m + b)
plt.plot(x_result, y_result)
plt.show()

