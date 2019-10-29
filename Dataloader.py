import os
import cv2
from tqdm import tqdm
import imghdr
import pickle

class ImageDataset(object):
    def __init__(self, test_dir, train_dir, mode, config_dir):
        super(ImageDataset, self).__init__()
        self.test_dir = os.path.expanduser(test_dir)
        self.train_dir = os.path.expanduser(train_dir)
        self.mode = mode
        self.config_dir = os.path.expanduser(config_dir)
        self.testpaths = self.__load_files_from_dir(self.test_dir)
        self.trainpaths = self.__load_files_from_dir(self.train_dir)
        if len(self.testpaths) != len(self.trainpaths):
            raise Exception('The total numbers of test and train cases should be same!')

    def __is_txtfile(self, filepath):
        filepath = os.path.expanduser(filepath)
        return filepath[-4:] == '.txt'

    def __if_pfile(self, filepath):
        filepath = os.path.expanduser(filepath)
        return filepath[-2:] == '.p'

    def __load_files_from_dir(self, dirpath):
        datapaths = []
        dirpath = os.path.expanduser(dirpath)

        for path in os.listdir(dirpath):
            if self.mode == 'txt' and self.__is_txtfile(path):
                datapaths.append(path)

        return datapaths

    def __str2list(self, data):
        data = list(data)
        temp = ''
        res = []
        for item in data:
            if item == ' ':
                res.append(float(temp))
                temp = ''
            elif item == '\n':
                continue
            else:
                temp += item
        return res

    def Data_loader(self):
        res = []
        test = []
        train = []
        final = []

        if self.mode == 'txt':
            pbar = tqdm(total = len(self.testpaths), desc = 'loading valid data(txt mode)...')
            for i in range(len(self.testpaths)):
                testpath = os.path.join(self.test_dir, self.testpaths[i])
                trainpath = os.path.join(self.train_dir, self.trainpaths[i])
                #read test data
                f = open(testpath)
                temp = f.readline()
                while temp:
                    temp = self.__str2list(temp)
                    res.append(temp)
                    temp = f.readline()
                test.append(res)
                res = []
                f.close()
                #read train data
                f = open(trainpath)
                temp = f.readline()
                while temp:
                    temp = self.__str2list(temp)
                    res.append(temp)
                    temp = f.readline()
                train.append(res)
                res = []
                f.close()
                pbar.update()

            pbar.close()
            #final[0] is test data, final[1] is train data
            final.append(test)
            final.append(train)
            config_dir = os.path.expanduser(self.config_dir)
            #save .p file under txt mode
            if os.path.exists(config_dir) == False:
                os.makedirs(config_dir)
            cpath = config_dir + '\\final.p'
            with open(cpath, 'wb') as file:
                pickle.dump(final, file)
        
        elif self.mode == 'p':
            cpath = self.config_dir
            with open(cpath, mode = 'rb') as file:
                final = pickle.load(file)
                    
        return final
        



            
            
