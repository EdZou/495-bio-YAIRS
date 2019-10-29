# debug


# calculate each image using multi-thread

# thread_num = 4
# # generateTemplates(IMAGES_PATH, TEMPLATES_PATH)
# threads = []
# for i in range(thread_num):
#     ti = threading.Thread(target=generateTemplatesMT,args=(thread_num, i, ALL_IMAGES_PATH, TEMPLATES_PATH))
#     threads.append(ti)

# for t in threads:
#     t.setDaemon(True)
#     t.start()
# t.join()



# test parse object path(PASS)
# mp, ep = parseObjpath('C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/mydataset/LG4000-2010-04-27_29/2010-04-27_29/02463')
# print(mp),print(ep)

# test parse metadata (PASS)
# metadata = parseMetadata('C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/mydataset/LG4000-2010-04-27_29/2010-04-27_29/02463/02463.txt')
# print(metadata['02463d2873']['eye'])

# test match on original matlab funciton(PASS)
# eye1 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/demo_dataset/02463/02463d2873.tiff'
# eye2 = 'C:/Users/Donnie/Desktop/NU/EE395_Biometrics/495-bio-YAIRS/demo_dataset/04233/04233d2600.tiff'
# res = matchImage(eye1, eye1)
# print(res)