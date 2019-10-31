# Dataset structure:
#   ----Object Index
#       ----metadata.txt
#       ----eyeimage1.tiff
#       ----eyeimage2.tiff

# change this path to adjust to your env
PROJECT_PATH = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/'

SRC_PATH = PROJECT_PATH + 'src/'
DATASETS_PATH = SRC_PATH + 'datasets/'
ARRAYS_PATH = SRC_PATH + 'arrays/'

# the path of the '4000-2010-04-27' dataset
LG4000_DATASET = DATASETS_PATH + 'LG4000-2010-04-27_29/2010-04-27_29'
# the path of the '2200-2010-04-27' dataset
LG2200_DATASET = DATASETS_PATH + '/LG2200-2010-04-27_29/2010-04-27_29'
# the path of the 'demo' dataset, including 30 
DEMO_DATASET = DATASETS_PATH + '/demo_dataset'
# the path of the 'tiny' dataset, including 7
SMALL_DATASET = DATASETS_PATH + '/small_dataset'
# the path of the 'tiny' dataset, including 3
TINY_DATASET = DATASETS_PATH + '/tiny_dataset'

CLEAN_4000 = DATASETS_PATH + '/cleandata' + '/4000'
CLEAN_22002 = DATASETS_PATH + '/cleandata' + '/22002'

CLEAN_GALLERY = DATASETS_PATH + '/cleandata' + '/gallery'
CLEAN_TEST= DATASETS_PATH + '/cleandata' + '/test'

HAMMING_ARRAY = ARRAYS_PATH + 'hamming_array'
CORRECT_ARRAY = ARRAYS_PATH + 'correct_array'