
import cv2
import xml.etree.ElementTree as ET
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-img", "--image_path", dest="image_path", help="Specify the image path",
                    required=True)
parser.add_argument("-xml", "--xml_path", dest="xml_path", help="Specify the xml path", required=True)
parser.add_argument("-cascade_xml", "--cascade_xml", dest="cascade_xml", help="Specify the cascade_xml file path", required=True)
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
if args.cascade_xml is None:
    print("Please specify the cascade_xml path")
    print("use the -h option to see usage information")
    sys.exit(2)
else:
    cascade_xml_path = args.cascade_xml

class Space:
    def __init__(self):
        self.id = 0
        self.occupied = 0
        self.rotatedRect = self.rotatedRect()
        self.contour = self.contour()

    def __repr__(self):
        return repr(vars(self))

    class rotatedRect:
        def __init__(self):
            self.center = self.center()
            self.size = self.size()
            self.angle = self.angle()

        def __repr__(self):
            return repr(vars(self))

        class center:
            def __init__(self):
                self.x = 0
                self.y = 0

            def __repr__(self):
                return repr(vars(self))

        class size:
            def __init__(self):
                self.w = 0
                self.h = 0

            def __repr__(self):
                return repr(vars(self))

        class angle:
            def __init__(self):
                self.d = 0

            def __repr__(self):
                return repr(vars(self))

    class contour:
        def __init__(self):
            self.pointArr = []
            self.point = self.point()

        def __repr__(self):
            return repr(vars(self))

        class point:
            def __init__(self):
                self.x = 0
                self.y = 0

            def __repr__(self):
                return repr(vars(self))


class FileInfo:
    #  put the same file together, and sequentially.
    def __init__(self):
        self.name = ""
        self.image_path = ""
        self.xml_path = ""

    def __repr__(self):
        return repr(vars(self))

class CarPosition:
    def __init__(self):
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

    def __repr__(self):
        return repr(vars(self))

class Space_xml:
    def __init__(self):
        self.id = 0
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
    def __repr__(self):
        return repr(vars(self))

class DetectCar:
    def __init__(self):
        self.id = 0

    def __repr__(self):
        return repr(vars(self))

def detect_parking_lot(image_path, xml_path, cascade_xml):
    space_arr = []
    tree = ET.ElementTree(file=xml_path)
    the_parkinglot = []
    car_cascade = cv2.CascadeClassifier(cascade_xml)

    for elem_space in tree.iter(tag='space'):
        new_space = Space()
        new_space.id = int(elem_space.attrib['id'])


        #  because some occupied didn't have the value, so we don't know if there is a car or not, so we crop the image
        #  base on the image has occupied value.
        try:
            new_space.occupied = int(elem_space.attrib['occupied'])
        except:
            print("[Exception] There is no field 'occupied' in xml where space_id = {0} path = {1}".format(new_space.id, xml_path))

        # get each element from xml file
        for elem_rotatedRect in elem_space.iter(tag='rotatedRect'):
            for elem_center in elem_rotatedRect.iter(tag='center'):
                new_space.rotatedRect.center.x = int(elem_center.attrib['x'])
                new_space.rotatedRect.center.y = int(elem_center.attrib['y'])
            for elem_size in elem_rotatedRect.iter(tag='size'):
                new_space.rotatedRect.size.w = int(elem_size.attrib['w'])
                new_space.rotatedRect.size.h = int(elem_size.attrib['h'])
            for elem_angle in elem_rotatedRect.iter(tag='angle'):
                new_space.rotatedRect.angle.d = int(elem_angle.attrib['d'])

        for elem_contour in elem_space.iter(tag='contour'):
            for elem_point in elem_contour.iter(tag='point'):
                new_point = Space.contour.point()
                new_point.x = int(elem_point.attrib['x'])
                new_point.y = int(elem_point.attrib['y'])
                new_space.contour.pointArr.append(new_point)

        space_arr.append(new_space)

    all_xml_car = []
    detect_img = cv2.imread(image_path)
    gray = cv2.cvtColor(detect_img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    print('The parking space id for empty')
    i = 1
    # because we have four x and value, and we want to get them.
    for index, space in enumerate(space_arr):
        min_x = 999999  # set min_x very large to let any point.x smaller than min_x
        max_x = 0  # set max_x equal 0 to let any point.x bigger than max_x
        min_y = 999999
        max_y = 0
        
        for point in space.contour.pointArr:
            # we want to find the minimum x, y and maximum x, y
            # if point.x smaller than min_x, we replace the min_x
            # For example, in id=4, 1.x="453" y="369" 2.x="543" y="386" 3.x="573" y="334" 4.x="446" y="304"
            if point.x < min_x:
                min_x = point.x
            if point.y < min_y:
                min_y = point.y
            if point.x > max_x:
                max_x = point.x
            if point.y > max_y:
                max_y = point.y
        space_xml = Space_xml()
        space_xml.id = space.id
        space_xml.min_x = min_x
        space_xml.min_y = min_y
        space_xml.max_x = max_x
        space_xml.max_y = max_y
        if space.occupied == 0:
            print('id: ', space.id,' total number',i)
            i = i+1
        the_parkinglot.append(space_xml)
    print('======================================')
        #cv2.imwrite('/Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/car_detection/pos3000neg10000/parking2_rainy_result04.jpg', xml_area)
        # print(xml_area)
    for (x, y, w, h) in cars:
        #img1 = cv2.rectangle(detect_img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        car = CarPosition()
        car.min_x = x
        car.min_y = y
        car.max_x = x+w
        car.max_y = y+h
        all_xml_car.append(car)
    #print(all_xml_car)
    print('The id for the empty lot been detected ')
    detect_car = []
    i = 1
    for parking_space in the_parkinglot:
        max_percentage = 0
        for car in all_xml_car:
            percentage = similarityPercentage(parking_space, car)
            #print(percentage)
            if percentage >= 0.3 and percentage > max_percentage:
                max_percentage = percentage
        if max_percentage == 0:
            detect_car = DetectCar()
            detect_car.id = parking_space.id

            print(detect_car, i)
            i += 1


def similarityPercentage(parking_space, car):

    xA = max(parking_space.min_x, car.min_x)
    yA = max(parking_space.min_y, car.min_y)
    xB = min(parking_space.max_x, car.max_x)
    yB = min(parking_space.max_y, car.max_y)

    if not ((xA > xB) or (yA > yB)):

        interArea = (xB - xA + 1) * (yB - yA + 1)

        boxAArea = (parking_space.max_x - parking_space.min_x + 1) * (parking_space.max_y - parking_space.min_y + 1)
        boxBArea = (car.max_x - car.min_x) * (car.max_y - car.min_y)
        percentage = interArea / float(boxAArea+boxBArea - interArea)

        return percentage
    return 0

detect_parking_lot(image_path, xml_path, cascade_xml_path)

#/Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/xml/pos3000neg10000/Haar/cascade.xml







