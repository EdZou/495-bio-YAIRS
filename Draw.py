from matplotlib import pyplot as plt
import numpy as np
import pylab as pl
from scipy import interpolate
from tqdm import tqdm
import os
import pickle
from scipy.spatial.distance import hamming
import copy

class Drawfunc(object):
    def __init__(self, raw, res_dir, mode, hamming):
        super(Drawfunc, self).__init__()
        self.raw = raw
        if len(raw[0]) != len(raw[1]):
            raise Exception('test and train data should be in same length!')
        self.mode = mode
        self.hamming = hamming
        if res_dir == None:
            raise Exception('result directory cannot be None!')
        self.res_dir = os.path.expanduser(res_dir)
        self.score = self.__get_matrix()

    def __get_score(self, raw_v, raw_t):
        #raw_v is the verification sample, raw_test is the test sample
        #calculating hamming distance
        if len(raw_v) != len(raw_t) or len(raw_v[0]) != len(raw_t[0]):
            raise Exception('The shape of raw data should be same!')
        raw_v = (np.array(raw_v)*255).astype('uint8')
        raw_t = (np.array(raw_t)*255).astype('uint8')
        count = 0
        total = len(raw_v)*len(raw_v[0])
        
        for i in range(len(raw_v)):
            for j in range(len(raw_v[i])):
                if abs(raw_v[i][j]-raw_t[i][j]) <= self.hamming:
                    count += 1
        return count/total
    
    '''
    def __get_true(self):
        if self.mode:
            res = []
            totaln = 0
            for i in range(len(self.raw)):
                n = len(self.raw[i])
                totaln += (n*(n-1))/2
            pbar = tqdm(total = int(totaln), desc = 'Calculating True Score...')
            
            for i in range(len(self.raw)):
                for j in range(len(self.raw[i])-1):
                    for k in range(j+1, len(self.raw[i])):
                        res.append(self.__get_score(self.raw[i][j], self.raw[i][k]))
                        pbar.update()
            pbar.close()
            if os.path.exists(self.res_dir) == False:
                os.makedirs(self.res_dir)
            cpath = self.res_dir + '\\True_score.p'
            with open(cpath, 'wb') as file:
                pickle.dump(res, file)
        else:
            cpath = self.res_dir + '\\True_score.p'
            with open(cpath, 'rb') as file:
                res = pickle.load(file)
        return res

    def __get_false(self):
        if self.mode:
            res = []
            totaln = 0
            for i in range(len(self.raw)-1):
                n = len(self.raw[i])
                totaln += n
            pbar = tqdm(total = totaln, desc = 'Calculating False Score...')
            
            for i in range(len(self.raw)-1):
                for j in range(len(self.raw[i])):
                    for k in range(i, len(self.raw)):
                        for p in range(len(self.raw[k])):
                            res.append(self.__get_score(self.raw[i][j], self.raw[k][p]))
                    pbar.update()
            pbar.close()
            if os.path.exists(self.res_dir) == False:
                os.makedirs(self.res_dir)
            cpath = self.res_dir + '\\False_score.p'
            with open(cpath, 'wb') as file:
                pickle.dump(res, file)
        else:
            cpath = self.res_dir + '\\False_score.p'
            with open(cpath, 'rb') as file:
                res = pickle.load(file)
        return res
    '''

    def __get_matrix(self):
        #get 220*220 score matrix
        matrix = []
        temp = []
        if self.mode:
            print(len(self.raw[0]), len(self.raw[1]))
            pbar = tqdm(total = len(self.raw[0])*len(self.raw[1]), desc = 'Calculating Score Matrix...')
            for i in range(len(self.raw[0])):
                for j in range(len(self.raw[1])):
                    temp.append(self.__get_score(self.raw[0][i], self.raw[1][j]))
                    pbar.update()
                matrix.append(temp)
                temp = []
            pbar.close()
            print(matrix)
            if os.path.exists(self.res_dir) == False:
                os.makedirs(self.res_dir)
            cpath = self.res_dir + '\\Score_matrix.p'
            with open(cpath, 'wb') as file:
                pickle.dump(matrix, file)

        else:
            cpath = self.res_dir + '\\Score_matrix.p'
            with open(cpath, 'rb') as file:
                matrix = pickle.load(file)
        return matrix
            

    def Draw_ROC(self):
        true = []
        false = []
        #build TMR and FMR list
        for i in range(len(self.score)):
            for j in range(len(self.score[0])):
                if i == j:
                    true.append(self.score[i][j])
                else:
                    false.append(self.score[i][j])
        true_len = len(true)
        false_len = len(false)

        tmr = []
        fmr = []
        pbar = tqdm(total = 101, desc = 'Calculating ROC parameters...')
        for i in range(101):
            true_c = 0
            false_c = 0
            standard = 1 - i/100
            for score in true:
                if score >= standard:
                    true_c += 1
            tmr.append(true_c/true_len)

            for score in false:
                if score >= standard:
                    false_c += 1
            fmr.append(false_c/false_len)
            pbar.update()
        pbar.close()
        print(true_len)
        print(false_len)

        plt.plot(fmr, tmr, '-b', label = 'ROC Curve')
        plt.xlabel('FMR')
        plt.ylabel('TMR')
        plt.savefig('ROC_Curve.jpg')
        plt.show()
            
        return

    def Draw_Distribution(self):
        true = []
        false = []
        #build TMR and FMR list
        for i in range(len(self.score)):
            for j in range(len(self.score[0])):
                if i == j:
                    true.append(self.score[i][j])
                else:
                    false.append(self.score[i][j])
        true_len = len(true) #220
        false_len = len(false) #48400 - 220
        print(true_len, false_len)
        
        
        true.sort()
        false.sort()

        ytrue = []
        yfalse = []

        tstart = 0
        fstart = 0
        
        for i in range(21):
            standard = i*0.05
            tempt = tstart
            tempf = fstart
            if tstart < true_len - 1:
                while true[tstart] <= standard:
                    tstart += 1
                    if tstart >= true_len:
                        break
            ytrue.append((tstart - tempt)/true_len)
            if fstart < false_len - 1:
                while false[fstart] <= standard:
                    fstart += 1
                    if fstart >= false_len:
                        break
            yfalse.append((fstart - tempf)/false_len)

        x = np.arange(0, 1.05, 0.05)
        
        plt.plot(x, ytrue, '-r', label = 'Genuine')
        plt.plot(x, yfalse, '-b', label = 'Imposter')


        plt.title('Distribution')
        plt.xlabel('Score')
        plt.ylabel('Frequency')

        plt.xlim(0.0, 1.1)
        plt.ylim(0.0, 1.0)

        plt.legend()
        plt.savefig('Distribution.jpg')
        plt.show()
        return

    def Draw_CMC(self):
        #first sort matrix score in the order of descending
        #then check whether the lowest score has been less than the score of true
        #find how many false cases should be taken to get the true cases
        matrix = copy.deepcopy(self.score)
        for i in range(len(matrix)):
            matrix[i].sort(reverse = True)
        x = np.arange(0,len(matrix) + 1)
        y = [0]
        for j in range(len(matrix[0])):
            count = 0
            for i in range(len(matrix)):
                if matrix[i][j] <= self.score[i][i]:
                    count += 1
            y.append(count/len(matrix))

        plt.plot(x, y, '-b', label = 'CMC Curve')
        plt.xlabel('CMC')
        plt.ylabel('RANK')
        plt.savefig('CMC_Curve.jpg')
        plt.show()
                
