import sys
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-img", "--image_path", dest="image_path", help="Specify the image path",
                    required=True)

args = parser.parse_args()

if args.image_path is None:
    print("Please specify the image path")
    print("use the -h option to see usage information")
    sys.exit(2)
else:
    image_path = args.image_path

#image_path = '/Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/new_positive_LBP/'

fns = os.listdir(image_path)
with open('positive_LBP.txt', 'w') as f:
    for fn in fns:
        path = os.path.join(image_path, fn)
        # print('{}\n'.format(path+' 1 0 0 20 20'))
        f.write('{}\n'.format(path + ' 1 0 0 20 20'))