# coding=utf-8
import matlab.engine
import os
import numpy as np
import math
import threading
import matplotlib.pyplot as plt
import argparse
import paths
from scipy.interpolate import make_interp_spline, BSpline
from tools import *





# get the TPR and FPR of one given threshold
def testThreshold(hammingArray, correctArray, threshold):
    # print('testing threshold:{0}'.format(threshold))

    size, size = hammingArray.shape
    testArray = np.array((size, size))

    allPositiveNum = 0
    truePositiveNum = 0
    trueNegativeNum = 0
    falsePositiveNum = 0
    falseNegativeNum = 0

    for i in range(size):
        for j in range(size):
            correctResult = correctArray[i, j]

            testResult = 1 if hammingArray[i,j] <= threshold else 0

            truePositive = 1 if (testResult == 1 and correctResult == 1) else 0
            trueNegative = 1 if (testResult == 0 and correctResult == 0) else 0
            falsePositive = 1 if (testResult == 1 and correctResult == 0) else 0
            falseNegative = 1 if (testResult == 0 and correctResult == 1) else 0

            allPositiveNum += testResult

            truePositiveNum += truePositive
            trueNegativeNum += trueNegative
            falsePositiveNum += falsePositive
            falseNegativeNum += falseNegative

    # print(truePositiveNum, falsePositiveNum, allPositiveNum)
    TPR = truePositiveNum/(truePositiveNum + falseNegativeNum)
    FPR = falsePositiveNum/(falsePositiveNum + trueNegativeNum)
    return TPR, FPR 
            
def drawROC(hammingArray, correctArray):
    X = [] 
    Y = []
    R = []
    for t in range(0, 1000):
        threshold = t/1000
        tp, fp = testThreshold(hammingArray, correctArray, threshold)
        # print('Testing {0}, TPR: {1}, FPR:{2}'.format(threshold, tp, fp))
        X.append(fp)
        Y.append(tp)
        R.append([fp, tp])
    np.savetxt('R.txt', R)
    plt.plot(X, Y)
    plt.show()

def drawDistributions(hammingArray, correctArray, smooth=False):
    # interval is 0.02
    intervalNum = 20
    dist = list(range(intervalNum))
    genuineDistribution = [0 for i in range(intervalNum)]
    imposterDistribution = [0 for i in range(intervalNum)]
    size, _ = hammingArray.shape
    for i in range(size):
        for j in range(size):
            score = hammingArray[i, j]
            if not math.isnan(score) and score != 0.0 and score != 1.0:
                # print(score)
                intervalIndex = int(score//(1/intervalNum))

                genuine = 1 if correctArray[i, j] == 1 else 0
                imposter = 1 if correctArray[i, j] == 0 else 0

                genuineDistribution[intervalIndex] += genuine
                imposterDistribution[intervalIndex] += imposter
    normalize = lambda L: list(map(lambda x: x/sum(L), L))
    genuineDistribution = normalize(genuineDistribution)
    imposterDistribution = normalize(imposterDistribution)
    # print(genuineDistribution, imposterDistribution)

    # draw the plot
    X = [0.02*i for i in range(intervalNum)]
    if smooth:
        Xnew = np.linspace(max(X), min(X), 100)

        g = make_interp_spline(X, genuineDistribution, k=3)
        i = make_interp_spline(X, imposterDistribution, k=3)

        genuineDistribution = g(Xnew)
        imposterDistribution = i(Xnew)
        plt.plot(Xnew, genuineDistribution)
        plt.plot(Xnew, imposterDistribution)
        plt.show()
    else:
        plt.plot(X, genuineDistribution)
        plt.plot(X, imposterDistribution)
        plt.show()

    # return genuineDistribution, imposterDistribution


if __name__ == "__main__":  
    parser = argparse.ArgumentParser() 

    # calculateDataset(PATH_4000)
    # calculateDataset(PATH_2200)

    # getHammingDistanceArray(TINY_DATASET)

    hammingArray = np.loadtxt('C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/hamming_30.txt')
    correctArray = np.loadtxt('C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/correct_30.txt')

    # drawROC(hammingArray, correctArray)
    drawDistributions(hammingArray, correctArray, False)