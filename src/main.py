# coding=utf-8
import matlab.engine
import os
import numpy as np

TEST_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/src/images/Test/'
IMAGES_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/src/images/LG-02463/'
DIAGNOSTICS_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/src/diagnostics/'
TEMPLATES_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/src/templates/'

def generateOneTemplate(eyeimage):
    eng = matlab.engine.start_matlab()
    template = eng.createiristemplate(IMAGES_PATH + '02463d1914.tiff', '')
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
            


if __name__ == "__main__":  
    generateTemplates(IMAGES_PATH, TEMPLATES_PATH)