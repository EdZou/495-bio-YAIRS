import matlab.engine
import os
import numpy as np
import math
import threading

# parse the txt of a metadata file
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

# parse a subfilefolder(a object)
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

# def parseDataset(datasetPath):
#     # eng = matlab.engine.start_matlab()
#     objPaths = os.listdir(datasetPath)
#     for objPath in objPaths:
#         metadataPath, eyeimagePaths = parseObj(objPath)
#         metadata = parseMetadata(metadata)

# get hamming distance of 2 images
def getHammingDistance(eyeimage_1, eyeimage_2, eng):
    res = eng.match(eyeimage_1, eyeimage_2)
    return res

# get all hamming distances of images in a dataset
# and write to a file
def getHammingDistanceArray(datasetPath):
    # parse the dataset path
    objPaths = os.listdir(datasetPath)
    objPaths = list(map(lambda x:datasetPath+'/'+x, objPaths))
    allEyeImages = []
    allMetadata = {}
    for objPath in objPaths:
        # parse the metadata and eyeimages paths
        metadataPath, eyeimagePaths = parseObj(objPath)
        metadata = parseMetadata(metadataPath)
        allMetadata = {**allMetadata, **metadata}
        # get indexes
        for eyeimagePath in eyeimagePaths:
            # print(eyeimagePath)
            allEyeImages.append(eyeimagePath)
    # print(allMetadata['04649d416']['color'])

    # initialize
    size = len(allEyeImages)
    indexes = []
    hammingArray = np.ones((size, size))
    correctArray = np.zeros((size, size))
    eng = matlab.engine.start_matlab()
    progress = 0

    # calculate all images pair
    for i_1, eyeimage_1 in enumerate(allEyeImages):
        # record the index og images
        index_1 = eyeimage_1.split('/')[-1].split('.')[0]
        obj_1 = index_1.split('d')[0]
        indexes.append(index_1)
        # calculate the hamming distance of each pair of images
        for i_2, eyeimage_2 in enumerate(allEyeImages):
            index_2 = eyeimage_2.split('/')[-1].split('.')[0]
            obj_2 = index_2.split('d')[0]

            # record the progress
            progress += 1
            if progress % 100 == 0:
                print('calculating hd of {0} and {1}, {2}/{3}'.format(index_1, index_2, progress, size*size))
            # update the correct answer
            correctArray[i_1, i_2] = 1 if obj_1 == obj_2 else 0
            # update the hamming array
            # images of different eyes
            if allMetadata[index_1]['eye']!= allMetadata[index_2]['eye']:
                hammingArray[i_1, i_2] = 1
            # images of same index
            elif index_1 == index_2:
                hammingArray[i_1, i_2] = 0
            # images need to calculate
            elif hammingArray[i_1, i_2] == 1:
                hammingDistance = getHammingDistance(eyeimage_1, eyeimage_2, eng)
                hammingArray[i_1, i_2] = hammingDistance
                # print(hammingDistance)
            
    # record the hamming distance array 
    # and the 'correct answers'
    np.savetxt('hamming_30.txt', hammingArray)
    np.savetxt('correct_30.txt', correctArray)