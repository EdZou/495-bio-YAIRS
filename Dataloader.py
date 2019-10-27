import os
import cv2
from tqdm import tqdm
import imghdr
import pickle

class ImageDataset(object):
    def __init__(self, data_dir, mode, config_dir):
        super(ImageDataset, self).__init__()
        self.dirlen = len(data_dir)
        self.data_dir = os.path.expanduser(data_dir)
        self.mode = mode
        self.config_dir = os.path.expanduser(config_dir)
        self.datapaths = self.__load_files_from_dir(self.data_dir)

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
            if self.mode == '.p' and self.__is_pfile(path):
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
        final = []

        if self.mode == 'txt':
            pbar = tqdm(total = len(self.datapaths), desc = 'loading valid data(txt mode)...')
            for i in range(len(self.datapaths)):
                datapath = os.path.join(self.data_dir, self.datapaths[i])
                f = open(datapath)
                temp = f.readline()
                while temp:
                    temp = self.__str2list(temp)
                    res.append(temp)
                    temp = f.readline()
                final.append(res)
                f.close()
                config_dir = os.path.expanduser(self.config_dir)
                #save .p file under txt mode
                if os.path.exists(config_dir) == False:
                    os.makedirs(config_dir)
                cpath = config_dir + '\\' + self.datapaths[i][:-4] + '.p'
                with open(cpath, 'wb') as file:
                    pickle.dump(res, file)
                res = []
                pbar.update()

            pbar.close()

        elif self.mode == 'p':
            temp = ''
            record = ''
            res = []
            final = []
            pbar = tqdm(total = len(os.listdir(self.config_dir)), desc = 'loading valid data(p mode)...')
            for path in os.listdir(self.config_dir):
                #find the iris of same people
                if 'd' not in path:
                    continue
                if temp == '':
                    for cha in path:
                        if cha != 'd':
                            temp += cha
                        else:
                            break
                else:
                    for cha in path:
                        if cha != 'd':
                            record += cha
                        else:
                            break
                    if record != temp:
                        temp = record
                        final.append(res)
                        res = []
                    record = ''
                config_dir = os.path.join(self.config_dir, path)
                with open(config_dir, mode = 'rb') as file:
                    res.append(pickle.load(file))
                pbar.update()
            pbar.close()
                    
            cpath = self.config_dir + '\\final.p'
            with open(cpath, 'wb') as file:
                pickle.dump(final, file)

        elif self.mode == 'final':
            cpath = self.config_dir + '\\final.p'
            with open(cpath, mode = 'rb') as file:
                    final = pickle.load(file)
                    
        return final
        



            
            
