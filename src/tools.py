import matlab.engine
import os
import numpy as np
import math
import threading
import paths

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

# generate templates and masks for all images in a dataset
def calculateDataset(datasetPath):
    progress = 0
    eng = matlab.engine.start_matlab()
    # parse the dataset path
    objPaths = os.listdir(datasetPath)
    objPaths = list(map(lambda x:datasetPath+'/'+x, objPaths))
    allEyeImages = []
    allMetadata = {}
    for objPath in objPaths:
        progress += 1
        print('calculating mat of {0}, {1}/{2}'.format(objPath, progress, len(objPaths)))
        # parse the metadata and eyeimages paths
        metadataPath, eyeimagePaths = parseObj(objPath)
        metadata = parseMetadata(metadataPath)
        allMetadata = {**allMetadata, **metadata}
        # get indexes
        for eyeimagePath in eyeimagePaths: 
            eng.getTemplate(eyeimagePath)

# get hamming distance of 2 images
def getHammingDistance(eyeimage_1, eyeimage_2):
    eng = matlab.engine.start_matlab()
    res = eng.getHD(eyeimage_1, eyeimage_2)
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
            if progress % 10 == 0:
                print('calculating hd of {0} and {1}, {2}/{3}'.format(index_1, index_2, progress, size*size))
            # update the correct answer
            correctArray[i_1, i_2] = 1 if obj_1 == obj_2 else 0
            # update the hamming array
            # images of different eyes
            if allMetadata[index_1]['eye']!= allMetadata[index_2]['eye']:
                hammingDistance = eng.getHD(eyeimage_1, eyeimage_2)
                hammingArray[i_1, i_2] = hammingDistance
            # images of same index
            elif index_1 == index_2:
                hammingArray[i_1, i_2] = 0
            # images need to calculate
            elif hammingArray[i_1, i_2] == 1:
                hammingDistance = eng.getHD(eyeimage_1, eyeimage_2)
                hammingArray[i_1, i_2] = hammingDistance
                # print(hammingDistance)
            
    # record the hamming distance array 
    # and the 'correct answers'
    tag = 'shift20-20'
    np.savetxt('{0}{1}_{2}.txt'.format(paths.HAMMING_ARRAY, size, tag), hammingArray)
    np.savetxt('{0}{1}_{2}.txt'.format(paths.CORRECT_ARRAY, size, tag), correctArray)

def getHammingDistanceFromCleandata(cleandataPath):
    # parse the dataset path
    eyeimagePaths = os.listdir(cleandataPath)
    allEyeImages = []
    for eyeimagePath in eyeimagePaths:
        allEyeImages.append(cleandataPath+'/'+eyeimagePath)

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
            if progress % 10 == 0:
                print('calculating hd of {0} and {1}, {2}/{3}'.format(index_1, index_2, progress, size*size))
            # update the correct answer
            correctArray[i_1, i_2] = 1 if obj_1 == obj_2 else 0
            # update the hamming array
            # images of different eyes
            # images of same index
            if index_1 == index_2:
                hammingArray[i_1, i_2] = 0
            # images need to calculate
            elif hammingArray[i_1, i_2] == 1:
                hammingDistance = eng.getHD(eyeimage_1, eyeimage_2)
                hammingArray[i_1, i_2] = hammingDistance
                # print(hammingDistance)
            
    # record the hamming distance array 
    # and the 'correct answers'
    tag = 'shift8-8'
    np.savetxt('{0}{1}_{2}.txt'.format(paths.HAMMING_ARRAY, size, tag), hammingArray)
    np.savetxt('{0}{1}_{2}.txt'.format(paths.CORRECT_ARRAY, size, tag), correctArray)

def getHammingDistanceFromCleandata(galleryPath, testPath):
    galleryImagePaths = os.listdir(galleryPath)
    testImagePaths = os.listdir(testPath)
    
    galleryImagePaths = list(map(lambda x: galleryPath+'/'+x, galleryImagePaths))
    testImagePaths = list(map(lambda x:testPath+'/'+x, testImagePaths))

    # initialize
    size = len(galleryImagePaths)
    indexes = []
    hammingArray = np.ones((size, size))
    correctArray = np.zeros((size, size))
    eng = matlab.engine.start_matlab()
    progress = 0

    # calculate all images pair
    for i_1, eyeimage_1 in enumerate(testImagePaths):
        # record the index og images
        index_1 = eyeimage_1.split('/')[-1].split('.')[0]
        obj_1 = index_1.split('d')[0]
        indexes.append(index_1)
        # calculate the hamming distance of each pair of images
        for i_2, eyeimage_2 in enumerate(galleryImagePaths):
            index_2 = eyeimage_2.split('/')[-1].split('.')[0]
            obj_2 = index_2.split('d')[0]

            # record the progress
            progress += 1
            if progress % 1 == 0:
                print('calculating hd of {0} and {1}, {2}/{3}'.format(index_1, index_2, progress, size*size))
            # update the correct answer
            correctArray[i_1, i_2] = 1 if obj_1 == obj_2 else 0
            # update the hamming array
            hammingDistance = eng.getHD(eyeimage_1, eyeimage_2)
            hammingArray[i_1, i_2] = hammingDistance
            print(hammingDistance)
    tag = 'shift8-8'
    np.savetxt('{0}{1}_{2}.txt'.format(paths.HAMMING_ARRAY, size, tag), hammingArray)
    np.savetxt('{0}{1}_{2}.txt'.format(paths.CORRECT_ARRAY, size, tag), correctArray)

def fastTemplate(dataPath):
    eng = matlab.engine.start_matlab()
    imagePaths = os.listdir(dataPath)
    imagePaths = list(map(lambda x: '{0}/{1}'.format(dataPath, x), imagePaths))
    for i, imagePath in enumerate(imagePaths):
        print('[Calculating]: {0}, [{1}/{2}]'.format(imagePath, i+1, len(imagePaths)))
        polar_array = np.array(eng.fastTemplate(imagePath))

        index = imagePath.split('/')[-1].split('.')[0]
        saveFile = dataPath + '-tp/' + index + '.txt'
        print(saveFile)
        np.savetxt(saveFile, polar_array)        