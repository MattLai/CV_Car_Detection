import sys
import os
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-img", "--image_path", dest="image_path", help="Specify the image path",
                    required=True)
parser.add_argument("-des", "--des_path", dest="des_path", help="Specify the output path", required=True)


args = parser.parse_args()

#image_path = '/Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/positive/'
#destination_dir_path = "/Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/new_positive_LBP/"


if args.image_path is None:
    print("Please specify the image path")
    print("use the -h option to see usage information")
    sys.exit(2)
else:
    image_path = args.image_path

if args.des_path is None:
    print("Please specify the output path")
    print("use the -h option to see usage information")
    sys.exit(2)
else:
    destination_dir_path = args.des_path

os.makedirs(args.des_path)
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f
f = listdir_nohidden(image_path)
for fn in f:

    old_image_path = os.path.join(image_path, fn)
    img = cv2.imread(old_image_path)
    height, width, channels = img.shape

    if height > width:
        width = height
    else:
        height = width

    resize_img = cv2.resize(img, (20, 20), 0, 0, cv2.INTER_LINEAR)
    gray_img = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)

    new_file_name = args.des_path + fn

    cv2.imwrite(new_file_name, gray_img)




