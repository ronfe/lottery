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

def generateRandomRes(times, rsvBalls):
    out = main.estimateBestBalls(times)
    if rsvBalls >= 1:
        out = out[0:rsvBalls -1]
        tempOut = []
        for each in out:
            tempOut.append(string.atoi(each))
    else:
        out = []
        tempOut = []
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

generalRed = 0
generalBlue = 0
def compareResult(genRes, realRed, realBlue):
    # return a list with the first element indicates the exact red balls and the second indicates the blue one
    global generalRed, generalBlue
    genRed = genRes[0]
    guessedRed = 0
    for each in genRed:
        if each in realRed:
            guessedRed += 1
    genBlue = genRes[1]
    guessedBlue = 0
    if genBlue == realBlue:
        guessedBlue = 1

    generalRed += guessedRed
    generalBlue += guessedBlue

    return [guessedRed, 1]

award = [0] * 6
awardPrize = [10000000, 500000, 3000, 200, 10, 5]
def decideAward(guessedNumber):
    # return the award info
    global award, awardPrize
    tempText = ''
    if guessedNumber == [6, 1]:
        award[0] += 1
        tempText = 'First Prize'
    elif guessedNumber == [6, 0]:
        award[1] += 1
        tempText = 'Second Prize'
    elif guessedNumber == [5, 1]:
        award[2] += 1
        tempText = 'Third Prize'
    elif guessedNumber in [[5, 0], [4, 1]]:
        award[3] += 1
        tempText = 'Fourth Prize'
    elif guessedNumber in [[4, 0], [3, 1]]:
        award[4] += 1
        tempText = 'Fifth Prize'
    elif guessedNumber in [[2, 1], [1, 1], [0, 1]]:
        award[5] += 1
        tempText = 'Sixth Prize'
    else:
        tempText = 'No Prize'

    return tempText

def testing(thisLost, testType, trainTimes, resRed, resBlue):
    # testType: 1 for fixed result, 2 for random result
    main.recordLost(thisLost)

    a = generateRandomRes(trainTimes, testType)

    b = compareResult(a, resRed, resBlue)
    c = decideAward(b)
    t = str(b[0]) + 'red, ' + str(b[1]) + 'blue. ' + c
    return t


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
    testT = testing(curLost, 6, 20, redHistory[curTestIssue -1], blueHistory[curTestIssue -1])
    print testT
    # end testing
    testTimes += 1
    curTestIssue -= 1
print 'Test Ends'
print 'Altogether, ' + str(generalRed) + '/' + str(testTimes * 6) + ' red, and ' + str(generalBlue) + '/' + str(testTimes) + ' blue guessed.'
totalAward = 0
for i in range(0, 6):
    totalAward += award[i] * awardPrize[i]
print 'totalAward: ' + str(totalAward)
print award


print 'a'

# lost = [0, 0, 0, 22, 41, 1, 4, 2, 1, 1, 0, 4, 3, 9, 14, 5, 4, 2, 2, 14, 1, 3, 4, 3, 0, 13, 5, 3, 1, 8, 0, 5, 1, 0]
# main.recordLost(lost)
# print main.estimateBestBalls(100)