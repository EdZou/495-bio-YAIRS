import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse
import os
from Dataloader import ImageDataset
import pickle
from Draw import Drawfunc

'''
main function of Iris
developed by Cong Zou, 10/26/2019

To use it, open the terminal in Linux or cmd in windows
enter the directory of main.py, Dataloader.py and Segmentation.py
CAUTION: These three .py files should be in the same file folder
imread the img by changing the root
For instance, enter this order in terminal/cmd
python main.py --img.dir D:/files/image/joy1.bmp
to find the image.

e.g.
python main.py --oneimage_dir hand.jpg --res_dir results --train_mode --process_mode 6
'''


parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type = str, default = 'txtdataset')
parser.add_argument('--config_dir', type = str, default = 'config')
parser.add_argument('--final_dir', type = str, default = 'config\final.p')
parser.add_argument('--data_mode', type = str, choices = ['txt','p', 'final'], default = 'final')
parser.add_argument('--res_dir', type = str, default = 'results')
parser.add_argument('--train_mode', action = 'store_true', default = False)

def main(args):
    if args.data_mode == 'txt' or args.data_mode == 'final':
        dl1 = ImageDataset(args.data_dir, args.data_mode, args.config_dir)
        data = dl1.Data_loader()
    if args.data_mode == 'txt' or args.data_mode == 'p':
        dl2 = ImageDataset(args.data_dir, 'p', args.config_dir)
        data = dl2.Data_loader()
    print(len(data), len(data[0]))

    df = Drawfunc(data, args.res_dir, args.train_mode)
    df.Draw_ROC()

    '''
    
    #=====================save images results=============================
    if args.res_dir != None:
        args.res_dir = os.path.expanduser(args.res_dir)
        if args.oneimage_dir != None:
            args.res_dir = args.res_dir + '\\1img_results'
        else:
            args.res_dir = args.res_dir + '\\dataset_results'
            
        if os.path.exists(args.res_dir) == False:
            os.makedirs(args.res_dir)

        mode = ['\\RGB_', '\\NRGB_', '\\HSI_', '\\Gaussian_RGB_', '\\Gaussian_NRGB_', '\\Gaussian_HSI_']
        if args.process_mode > 3:
            threshold = args.g_threshold
        else:
            threshold = args.h_threshold
        imgpath = args.res_dir + mode[args.process_mode - 1] + str(threshold) + img_dir
        cv2.imwrite(imgpath, res*255)
    '''


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

    


