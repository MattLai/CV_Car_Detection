
import cv2
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-img", "--image_path", dest="image_path", help="Specify the image path",
                    required=True)
parser.add_argument("-xml", "--xml_path", dest="xml_path", help="Specify the xml path", required=True)
parser.add_argument("-output", "--output", dest="output", help="Specify the output file path", required=True)
parser.add_argument("-out_name", "--out_name", dest="out_name", help="Specify the output image name", required=True)

args = parser.parse_args()

if args.image_path is None:
    print("Please specify the image path")
    print("use the -h option to see usage information")
    sys.exit(2)
else:
    image_path = args.image_path
if args.xml_path is None:
    print("Please specify the xml path")
    print("use the -h option to see usage information")
    sys.exit(2)
else:
    xml_path = args.xml_path
if args.output is None:
    print("Please specify the output path")
    print("use the -h option to see usage information")
    sys.exit(2)
else:
    output_path = args.output
if args.out_name is None:
    print("Please specify the output image name")
    print("use the -h option to see usage information")
    sys.exit(2)
else:
    output_name = args.out_name

car_cascade = cv2.CascadeClassifier(xml_path)

def detect(filename):

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    #i = 1
    #j = 100
    #print('How many empty lots been detected:')
    for (x, y, w, h) in cars:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #print((x, y), (x+w, y+h), i)
    cv2.imwrite(output_path+output_name+'.jpg', img)

detect(image_path)

#  /Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/xml/pos300neg1000/LBP/cascade.xml

#  /Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/car_detection/pos3000neg10000/parking2_rainy_result26.jpg

#  /Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/PKLot/parking2/rainy/2012-09-21/2012-09-21_08_10_15.jpg'