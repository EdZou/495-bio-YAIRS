from matplotlib import pyplot as plt
import numpy as np
import pylab as pl
from scipy import interpolate
from tqdm import tqdm
import os
import pickle
from scipy.spatial.distance import hamming

class Drawfunc(object):
    def __init__(self, raw, res_dir, mode):
        super(Drawfunc, self).__init__()
        self.raw = raw
        self.mode = mode
        if res_dir == None:
            raise Exception('result directory cannot be None!')
        self.res_dir = os.path.expanduser(res_dir)
        self.true_score = self.__get_true()
        self.false_score = self.__get_false()

    def __get_score(self, raw_v, raw_t):
        #raw_v is the verification sample, raw_test is the test sample
        #calculating hamming distance
        if len(raw_v) != len(raw_t) or len(raw_v[0]) != len(raw_t[0]):
            raise Exception('The shape of raw data should be same!')
        raw_v = (np.array(raw_v)*255).astype('uint8')
        raw_t = (np.array(raw_t)*255).astype('uint8')
        raw_v = np.reshape(raw_v, (-1))
        raw_t = np.reshape(raw_t, (-1))
        
        res = hamming(raw_v, raw_t)
        return res

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

    def Draw_ROC(self):
        true = []
        false = []
        true_len = len(self.true_score)
        false_len = len(self.false_score)
        pbar = tqdm(total = 101, desc = 'Calculating ROC parameters...')
        for i in range(101):
            true_c = 0
            false_c = 0
            standard = 1 - i/100
            for score in self.true_score:
                if score >= standard:
                    true_c += 1
            true.append(true_c/true_len)

            for score in self.false_score:
                if score >= standard:
                    false_c += 1
            false.append(false_c/false_len)
            pbar.update()
        pbar.close()
        print(true_len)
        print(false_len)

        plt.plot(false, true, '-b', label = 'ROC Curve')
        plt.xlabel('FMR')
        plt.ylabel('TMR')
        #plt.savefig('ROC_Curve.jpg')
        plt.show()
            
            
        return
                

'''
x1 = np.array([0.08, 0.09, 0.10, 0.11, 0.12])
genuine = np.array([0, 1, 3, 1, 0])
x2 = np.array([0.47, 0.48, 0.49, 0.50, 0.51, 0.52, 0.53])
imposter = np.array([0, 1, 5, 8, 5, 1, 0])
'''
'''
x = np.arange(0,1.1,0.1)
y = np.arange(0,1.1,0.1)
genuine = np.zeros(100)
imposter = np.zeros(100)

genuine[10] = 0.2
genuine[11] = 0.8
genuine[12:] = 1

imposter[50] = 0.3
imposter[51] = 0.7
imposter[52] = 0.95
imposter[53:] = 1

#print(genuine)
#print(imposter)

xnew = np.zeros(2)
ynew = np.ones(2)
ynew[0] = 0
'''
#distribution
'''
plt.figure()

plt.subplot(1,2,1)
xnew1 = np.linspace(0.08,0.12,150)
xnew2 = np.linspace(0.47,0.53,150)
xnew = np.arange(0,1,1000)

cs1 = interpolate.CubicSpline(x1, genuine)
cs2 = interpolate.CubicSpline(x2, imposter)

genuine_new = cs1(xnew1)
imposter_new = cs2(xnew2)


plt.plot(xnew1, genuine_new, '-r', label = 'Genuine')
plt.plot(xnew2, imposter_new, '-b', label = 'Imposter')


plt.title('Distribution')
plt.xlabel('Score')
plt.ylabel('Frequency')

plt.xlim(0.0, 1.0)
plt.ylim(0.0, 9.0)

plt.legend()

plt.subplot(1,2,2)
plt.bar(x1,genuine, width = 0.01, color = 'r', label = 'Genuine')
plt.bar(x2,imposter, width = 0.01, color = 'b', label = 'Imposter')
plt.title('Distribution(Histogram)')
plt.xlabel('Score')
plt.ylabel('Frequency')

plt.xlim(0.0, 1.0)
plt.ylim(0.0, 9.0)
plt.legend()
'''
'''
x = [0.11, 0.47]
y = [1, 1]

plt.plot(x, y, '-b', label = 'Perfect ROC')
plt.xlim(0,1)
plt.xlabel('Score')
plt.ylabel('TMR')
#plt.savefig('Distribution.jpg')
plt.show()
'''
