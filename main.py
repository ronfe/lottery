__author__ = 'ronfe'

import os,string
import numpy as np
from scipy import stats

pwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(pwd)

originFile = open('last100.txt').readlines()
last100 = []
for each in originFile:
    t = each.strip()
    last100.append(t)

lostList = {}
totalLost = []
# the first one remains 0
currentLost = [0,6,2,21,40,0,3,1,0,0,2,3,2,8,13,4,3,1,1,13,0,2,3,2,1,12,4,2,0,7,8,4,0,5]

for i in range(99, -1, -1):
    tempBalls = last100[i]
    for each in tempBalls.split(','):
        tempIndex = string.atoi(each)
        if each not in lostList:
            lostList[each] = []
            lostList[each].append(currentLost[tempIndex])
            totalLost.append(currentLost[tempIndex])
            currentLost[tempIndex] = -1
        else:
            lostList[each].append(currentLost[tempIndex])
            totalLost.append(currentLost[tempIndex])
            currentLost[tempIndex] = -1

    currentLost = [x+1 for x in currentLost]

total = np.array(totalLost)
# totalNumbers = np.unique(total)
freqTable = stats.itemfreq(total)
k = 0
for each in freqTable:
    k += each[0] + each[1]

lmda = k / float(len(total))

xDistribution = np.random.poisson(lmda, 600)

# calculate horizonal probability
horP = {}
xItemFreq = stats.itemfreq(xDistribution)

for each in lostList:
    ballIndex = string.atoi(each)
    lostTimes = currentLost[ballIndex]
    for eachOne in xItemFreq:
        if eachOne[0] == lostTimes:
            tempP = eachOne[1] / 600.0
            horP[each] = tempP
            break
    if each not in horP:
        horP[each] = 1.0 / 600.0


# calculate vertical probability
verP = {}

for each in lostList:
    tempFreq = np.array(lostList[each])
    tempItemFreq = stats.itemfreq(tempFreq)
    k = 0
    for eachOne in tempItemFreq:
        k += eachOne[0] * eachOne[1]

    lmda = k / float(len(tempFreq))
    tempDistro = np.random.poisson(lmda, len(tempFreq))
    tTempDistro = stats.itemfreq(tempDistro)
    index = string.atoi(each)
    for tempI in tTempDistro:
        if tempI[0] == currentLost[index]:
            verP[each] = tempI[1] / float(len(tempFreq))
            break
    if each not in verP:
        verP[each] = 1 / float(len(tempFreq))

# Result
result = {}
for each in horP:
    tempResult = horP[each] * verP[each]
    result[each] = tempResult
sortedRes = sorted(result.iteritems(), key=lambda d:d[1], reverse = True)

outList = list(sortedRes)
for each in outList:
    print each


