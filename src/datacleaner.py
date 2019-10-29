# coding=utf-8
import matlab.engine
import os
import numpy as np
import math
import threading
import shutil

path2200 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/mydataset/LG2200-2008-03-11_13/2008-03-11_13'
path22002 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/mydataset/LG2200-2010-04-27_29/2010-04-27_29'
path4000 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/mydataset/LG4000-2010-04-27_29/2010-04-27_29'
target2200 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/cleandata/2200'
target22002 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/cleandata/22002'
target4000 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/cleandata/4000'

def parseMetadata(metadataPath):
    tmp_res = [{}]
    res = {}
    with open(metadataPath) as f:
        lines = f.readlines()
        index = 0
        for line in lines:
            line = line.strip()
            if len(line):
                key, typ, value = line.split('\t')
                # print('{0} {1} {2}'.format(key, typ, value))
                tmp_res[index][key] = value
            else:
                tmp_res.append({})
                index += 1
        for metadata in tmp_res:
            if 'sequenceid' in metadata:
                sequenceid = metadata['sequenceid']
                res[sequenceid] = metadata
    return res

def parseObj(objPath):
    metadataPath = ''
    eyeimagePaths = []
    filenames = os.listdir(objPath)
    for filename in filenames:
        name, subfix = filename.split('.')[0:2]
        if subfix == 'txt':
            metadataPath = objPath+'/'+name+'.'+subfix
        elif subfix == 'tiff':
            eyeimagePath = objPath+'/'+name+'.'+subfix
            eyeimagePaths.append(eyeimagePath)
    return metadataPath, eyeimagePaths

def cleanData(rawDataPath, cleanDataPath):
    rawObj = os.listdir(rawDataPath)
    rawObj = list(map(lambda x:'{0}/{1}'.format(rawDataPath, x), rawObj))
    # print(rawObj)
    for obj in rawObj:
        metadataPath, eyeimagePaths = parseObj(obj)
        metadata = parseMetadata(metadataPath)
        for key in metadata:
            value = metadata[key]
            # print(value['eye'])
            if value['eye'] == 'Left':
                selectedImage = '{0}/{1}.tiff'.format(obj, key)
                targetImage = '{0}/{1}.tiff'.format(cleanDataPath, key)
                shutil.copyfile(selectedImage, targetImage)
                break

if __name__ == "__main__":
    cleanData(path22002, target22002)