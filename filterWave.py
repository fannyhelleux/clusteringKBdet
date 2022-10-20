import os
import cv2
import matplotlib.image

# From a directory of image treats them using CLAHE technique and creates a new folder containing the treated images

# Get the list of all files in the directory
path = input(
    "\nEnter the path of the folder containing the images that need to be sorted: \nex : C:/Users/33608/OneDrive - Fondation EPF/Desktop/ERI/Image processing/Boils/Images/Cluster 4/ \n ")
pathTreated = input(
    "\nEnter the path of the folder for the new treated images: \nex : C:/Users/33608/OneDrive - Fondation EPF/Desktop/ERI/Image processing/Boils/Images/Treated Images/ \n ")
print("Processing ...")
# Recovery of all the file's name located in the chosen directory
dir_list = os.listdir(path)

# Creation of an array containing the path of all the file in the directory
imgName_List = []
for i in dir_list:
    imgName_List.append(path + i)

# definition of the coefficient for the brightness modification
alpha = 0.8
beta = -50

pathTreated_Wave = pathTreated + 'Wave images'
os.mkdir(pathTreated_Wave)

for i in dir_list:
    imgPath = path + i
    # Reading the image from the present directory
    image = cv2.imread(imgPath)
    image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # The declaration of CLAHE
    # clipLimit -> Threshold for contrast limiting
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
    imgCLAHE = clahe.apply(image_bw)

    # Decrease of the brightness
    imgFinal = cv2.convertScaleAbs(imgCLAHE, alpha=alpha, beta=beta)

    # Saving of the treated image in the new folder
    new_path = pathTreated_Wave + '/' + i
    matplotlib.image.imsave(new_path, imgFinal)

print('Treated images saved in new folder')
