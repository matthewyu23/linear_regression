import os
try: 
    import pandas as pd
except (Exception): 
    os.system("pip3 install pandas --user")
    import pandas as pd
try: 
    import matplotlib.pyplot as plt
except (Exception): 
    os.system("pip3 install matplotlib --user")
    import matplotlib.pyplot as plt
import json
import requests



    
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
    print("\n\niterations = " + printIter + ", B = " + printB + ", M = " + printM + ", error = " + printError + "\n\n")
    return b, m




numberOfPlots = 1
print("Ticker: ")
userInput = input().split(" ")

index = 1
for x in userInput: 
    x_result = []
    y_result = []

    
    data = requests.get(f"https://api.worldtradingdata.com/api/v1/history?symbol={x}&sort=newest&api_token=Nn3T3dHhdxvMDtttmaFMpmsChWFyvcaFKViUiqjwFGixpv2Z24lUFSe6uscx")
    parsed = data.json()["history"]
    j = []
    k = []

    counter = 0
    for x in parsed: 
        j.append(counter)
        counter = counter + 1
        k.append(float(parsed[x]["open"]))
        
    k = k[::-1]


    jLearningRate = 0.1
    kLearningRate = 0.00000001
    iterations = 1000
    initialB = 0
    initialM = 0
    graphDomainMin = 0
    graphDomainMax= len(parsed)


    b, m = runLinearReg(j, k, jLearningRate, kLearningRate, iterations, initialB, initialM)
    plt.subplot(len(userInput), 1, index)
    plt.plot(j, k, "o", markersize = 2)
    for i in range(graphDomainMin, graphDomainMax): 
        x_result.append(i)
        y_result.append(i*m + b)

    plt.plot(x_result, y_result)
    index += 1
plt.show()
