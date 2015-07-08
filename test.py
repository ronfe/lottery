__author__ = 'ronfe'

import main
import os
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

constructText(383)
print 'a'

# lost = [0, 0, 0, 22, 41, 1, 4, 2, 1, 1, 0, 4, 3, 9, 14, 5, 4, 2, 2, 14, 1, 3, 4, 3, 0, 13, 5, 3, 1, 8, 0, 5, 1, 0]
# main.recordLost(lost)
# print main.estimateBestBalls(100)