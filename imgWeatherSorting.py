"""
This program sort through different images from a folder (path as input). First it calculates their average luminosity, their
luminosity variance as well as the number of pixel above a certain threshold (function : imgCalculation). Then it creates a
standardized dataframe (mean = 0 and standard dev =1) that is then clusterized using a k-mean method. The images are then
copied to new folder depending on their cluster numbers

Other sorting characteristics can be added if necessary (gradient mean, ect.)
"""

# Libraries import :
import os
import shutil
import cv2
import numpy as np
import pandas as pd
from skimage import color
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# Parameters :
# Modify the sensitivity to light of the algorithm (0<x<1)
thresh_whitePX = 0.9
# Number of cluster created by the algorithm
nb_cluster = 4

path = input(
    "\nEnter the path of the folder containing the images that need to be sorted: \nex : C:/Users/33608/OneDrive - Fondation EPF/Desktop/ERI/Shag image treatement/october2019/ \n ")
# Get the path of the directory containing the images

print("Processing ...")



def imgCalculation(imgName):
    # function taking a file name (RGB jpg image) as input, converting as B/W and returning the luminosity variance,
    # mean and number of pixel above thresh_whitePX

    # input : imgName (String)
    # output : varImg_grey, meanImg_grey, whitePX

    img = cv2.imread(imgName)

    # Conversion of the image to greyscale
    img_grey = color.rgb2gray(img)

    # Different calculations
    # Number of pixel whose luminosity is > thresh_whitePX
    whitePX = np.sum(img_grey >= thresh_whitePX)

    # Variance and average value of the luminosity
    varImg_grey = img_grey.var()
    meanImg_grey = img_grey.mean()

    return varImg_grey, meanImg_grey, whitePX

# Recovery of all the file's name located in the chosen directory
dir_list = os.listdir(path)

# Creation of an array containing the path of all the file in the directory
imgName_List = []
for i in dir_list:
    imgName_List.append(path + i)

# Creation of an array containing the variance of luminosity of each picture located in the directory
varList = []
meanList = []
whitePXList = []

res = [2]

# For each image calculate the different parameters and fill the specified list with those
for i in imgName_List:
    res = imgCalculation(i)
    varList.append(res[0])
    meanList.append(res[1])
    whitePXList.append(res[2])

# creates a dataframe containing the variances, means and number of white pixel superior to the threshold
df = pd.DataFrame({'Variances ': varList, 'Means': meanList, 'Number of white PX (<thresh_whitePX)': whitePXList})

# create scaled DataFrame where each variable has mean of 0 and standard dev of 1
scaled_df = StandardScaler().fit_transform(df)

"""
KMeans(init=’random’, n_clusters=8, n_init=10, random_state=None) where: 
    init: Controls the initialization technique. 
    n_clusters: The number of clusters to place observations in. 
    n_init: The number of initializations to  perform. The default is to run the k-means algorithm 10 times and return 
    the one with the lowest SSE. 
    random_state:  An integer value you can pick to make the results of the algorithm reproducible.
"""

# instantiate the k-means class
kmeans = KMeans(init="random", n_clusters=nb_cluster, n_init=10, random_state=1)
# fit k-means algorithm to data
kmeans.fit(scaled_df)

# append cluster assignments to original DataFrame and append file name and path
df['Cluster'] = kmeans.labels_
df['File name'] = dir_list
df['File path'] = imgName_List

# Transfer of the files to the new directories
# Creation of the nb_cluster new folder in the original folder
pathCluster_list = []
for i in range(nb_cluster):
    newFolderPath = path + 'Cluster ' + str(i + 1)
    pathCluster_list.append(newFolderPath)
    os.mkdir(newFolderPath)

# Transfer of each file to their new folder
for i in range(df.shape[0]):

    # Recovery
    clusterNB = df.iloc[i]['Cluster']
    filePath = df.iloc[i]['File path']
    fileName = df.iloc[i]['File name']

    for i in range(nb_cluster):
        if clusterNB == i:
            new_path = pathCluster_list[i] + '/' + fileName
            shutil.copy(filePath, new_path)
        else:
            next

print('Transfer completed')
