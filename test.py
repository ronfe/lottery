__author__ = 'ronfe'

import main
import os, string, random
pwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(pwd)

# Step1: read the testset file and record the result
redHistory = []
blueHistory = []
f = open('testset.txt').readlines()
for each in f:
    stripText = each.strip()
    red, blue = stripText.split('|')
    redHistory.append(red)
    blueHistory.append(blue)

# Step2: construct the test material
def constructText(startIndex):
    recordHistory = []
    for i in range(startIndex - 99, startIndex + 1):
        recordHistory.append(redHistory[i])

    g = open('test100.txt', 'w')
    for each in recordHistory:
        g.write(each + '\n')
    g.close()

def generateFixRes(times):
    out = main.estimateBestBalls(times)
    blue = random.randint(1, 16)
    if blue < 10:
        blue = '0' + str(blue)
    else:
        blue = str(blue)
    res = [out, blue]
    return res

def generateRandomRes(times):
    out = main.estimateBestBalls(times)
    out = out[0:2]
    tempOut = []
    for each in out:
        tempOut.append(string.atoi(each))
    while len(tempOut) < 6:
        thisR = random.randint(1, 33)
        if thisR not in tempOut:
            tempOut.append(thisR)
    out = []
    for each in tempOut:
        if each < 10:
            out.append('0' + str(each))
        else:
            out.append(str(each))
    blue = random.randint(1, 16)
    if blue < 10:
        blue = '0' + str(blue)
    else:
        blue = str(blue)
    res = [out, blue]
    return res

def testing(thisLost, testType, trainTimes):
    # testType: 1 for fixed result, 2 for random result
    main.recordLost(thisLost)
    if testType == 1:
        generateFixRes(trainTimes)
    else:
        generateRandomRes(trainTimes)




# Construct outer loop for testing
curTestIssue = len(redHistory)
initLost = [0, 5,7,6,1,0,6,0,11,4,2,1,0,5,3,7,0,4,2,13,9,1,2,4,3,3,3,1,0,2,10,6,0,9]
testTimes = 0
curLost = []
while curTestIssue >= 101:
    if testTimes == 0:
        curLost = initLost
    else:
        tempLost = curLost
        lastResult = redHistory[curTestIssue]
        for each in lastResult.split(','):
            tI = string.atoi(each)
            tempLost[tI] = -1
        curLost = [x + 1 for x in tempLost]

    constructText(curTestIssue - 1)
    # start testing

    # end testing
    testTimes += 1
    curTestIssue -= 1



print 'a'

# lost = [0, 0, 0, 22, 41, 1, 4, 2, 1, 1, 0, 4, 3, 9, 14, 5, 4, 2, 2, 14, 1, 3, 4, 3, 0, 13, 5, 3, 1, 8, 0, 5, 1, 0]
# main.recordLost(lost)
# print main.estimateBestBalls(100)