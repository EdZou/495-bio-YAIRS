    raw_images = list(map(lambda x:imagePath+'\\'+x, raw_images))
    image = cv2.imread(raw_images[0])