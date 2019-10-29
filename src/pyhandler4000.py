# coding=utf-8
import matlab.engine
import os
import numpy as np
import math
import threading
from tools import *

DEMO_DATASET = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/demo_dataset'
TINY_DATASET = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/tiny_dataset'
CLEAN2200_DATASET = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/cleandata/2200'
CLEAN4000_DATASET = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/cleandata/4000'
CLEAN4000_DATASET2 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/cleandata/4000_2'

TEN_IMAGES_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/mydataset/2008-10'
ALL_IMAGES_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/mydataset/2008-03-11_13'
TEST_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/src/images/Test/'
IMAGES_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/src/images/LG-04233/'
DIAGNOSTICS_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/src/diagnostics/'
TEMPLATES_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/src/templates/'

def list_all_files(rootdir):
    _files = []
    l = os.listdir(rootdir)
    for i in range(0,len(l)):
           path = os.path.join(rootdir,l[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    _files = list(map(lambda x:x.replace('\\', '/'), _files))
    return _files

def generateOneTemplate(eyeimage):
    eng = matlab.engine.start_matlab()
    template = eng.createiristemplate(IMAGES_PATH + '02463d1914.tiff', '')
    eng.quit()
    return template

def generateTemplates(imagesPath, templatesPath):
    eng = matlab.engine.start_matlab()
    # get all files in the path
    files = os.listdir(imagesPath)
    # select the eye images
    for f in files:
        flist = f.split('.')
        # if the file is an image
        if flist[1] == 'tiff':
            image_index, _ = flist
            image_path = imagesPath + '/' + f
            template_path = templatesPath + image_index + '-tp.txt'
            res = eng.createiristemplate(image_path, '')
            res = np.array(res)

            with open(template_path, 'w') as tf:
                for line in res:
                    for value in line:
                        tf.write(str(value))
                        tf.write(' ')
                    tf.write('\n')
    eng.quit()

def fastTemplate(dataPath):
    eng = matlab.engine.start_matlab()
    imagePaths = os.listdir(dataPath)
    imagePaths = list(map(lambda x: '{0}/{1}'.format(dataPath, x), imagePaths))
    for i, imagePath in enumerate(imagePaths):
        print('[Calculating]: {0}, [{1}/{2}]'.format(imagePath, i+1, len(imagePaths)))
        polar_array = np.array(eng.fastTemplate(imagePath))

        index = imagePath.split('/')[-1].split('.')[0]
        saveFile = CLEAN4000_DATASET + '-tp/' + index + '.txt'
        print(saveFile)
        np.savetxt(saveFile, polar_array)        

def generateTemplatesMT(tnum, tid, imagesPath, templatesPath):
    print('{0}/{1}'.format(tid, tnum))
    # get all files in the path
    # files = os.listdir(imagesPath)
    files = list_all_files(imagesPath)
    # print(files)
    eye_images = []
    # select the eye images and collect
    for f in files:
        flist = f.split('.')
        # if the file is an image
        if flist[-1] == 'tiff':
            eye_images.append(f)
    eng = matlab.engine.start_matlab()
    total_task = len(eye_images)
    each_task = math.ceil(total_task/tnum)
    thread_task = [each_task*tid, each_task*(tid+1)]
    print(thread_task)
    for i, f in enumerate(eye_images):
        if i >= thread_task[0] and i <= thread_task[1]:
            image_path = f
            f = f.split('/')[-1]
            image_index, _ = f.split('.')
            template_path = templatesPath + image_index + '-tp.txt'
            print('thread is {0}, task is {1}, total_thread:{2}, total_task:{3}\n'.format(tid, image_index, tnum, total_task))
            res = eng.createiristemplate(image_path, '')
            # res = eng.fastTemplate(image_path, '')
            res = np.array(res)

            with open(template_path, 'w') as tf:
                for line in res:
                    for value in line:
                        tf.write(str(value))
                        tf.write(' ')
                    tf.write('\n')
    eng.quit()
    

if __name__ == "__main__":  
    # testThreshold(0)
    fastTemplate(CLEAN4000_DATASET2)