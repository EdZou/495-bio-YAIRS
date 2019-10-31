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

    allPositiveNum = truePositiveNum = trueNegativeNum = falsePositiveNum = falseNegativeNum = 0

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
    for t in range(0, 1000):
        threshold = t/1000
        tp, fp = testThreshold(hammingArray, correctArray, threshold)
        # print('Testing {0}, TPR: {1}, FPR:{2}'.format(threshold, tp, fp))
        X.append(fp)
        Y.append(tp)
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
    X = [(1/intervalNum)*i for i in range(intervalNum)]
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

def Draw_CMC(hammingArray):
    #first sort matrix score in the order of descending
    #then check whether the lowest score has been less than the score of true
    #find how many false cases should be taken to get the true cases
    matrix = hammingArray.tolist()
    for i in range(len(matrix)):
        matrix[i].sort()
    x = np.arange(0,len(matrix) + 1)
    y = [0]
    for j in range(len(matrix[0])):
        count = 0
        for i in range(len(matrix)):
            if matrix[i][j] >= hammingArray[i][i]:
                count += 1
        y.append(count/len(matrix))

    plt.plot(x, y, '-b', label = 'CMC Curve')
    plt.ylabel('CMC')
    plt.xlabel('RANK')
    plt.show()

if __name__ == "__main__":  
    # TODO: parse args from command line
    # parser = argparse.ArgumentParser() 

    # STEP 0: calculate templates and masks of every images in a given dataset
    # and write to mat files in /diagnostics 

    # calculateDataset(paths.LG2200_DATASET)
    # calculateDataset(paths.LG4000_DATASET)

    # STEP 1: get the HammingDistanceArray (each element is the hd between img1 and img2) 
    # and save the hamming array and correct array (1 means the same obj, 0 means different) to .txt file

    # getHammingDistanceFromCleandata(paths.CLEAN_4000, paths.CLEAN_22002)

    # STEP 2: load hamming array and correct array from file

    tag = tag = 'shift8-8'
    hammingPath = '{0}{1}_{2}.txt'.format(paths.HAMMING_ARRAY, 220, tag)
    correctPath = '{0}{1}_{2}.txt'.format(paths.CORRECT_ARRAY, 220, tag)
    hammingArray = np.loadtxt(hammingPath)
    correctArray = np.loadtxt(correctPath)


    # STEP 3: draw the distribution and the ROC curve

    drawROC(hammingArray, correctArray)
    drawDistributions(hammingArray, correctArray, False)
    Draw_CMC(hammingArray)