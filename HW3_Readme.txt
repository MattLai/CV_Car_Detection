
Data set:The data set consists of images from three separate parking lots parking1a, parking1b and parking2. Each of the parking has data set sorted for three different scenarios cloudy, rainy and sunny. Each single day is represented by the folder, for example the folder (e.g. PKLot/parking/cloudy/2012-12-12/) contains multiple snapshot images (like 2012_12_12_10_00_05.jpg) and the corresponding ground truth file (like 2012_12_12_10_00_05.xml).                     
Ground Truth(.xml)Each image in the parking2 has 100 annotated parking spaces (see image below), along with the location, and occupancy information of the parking spot (Every image is supplemented with a ground truth file. For example (parking2/cloudy/2012-09-12/2012-09-12_06_05_16.jpg) has the ground truth file (parking2/cloudy/2012-09-12/2012-09-12_06_05_16.xml).


-------------------------------------------
1. Use howework3.py to generate the positive and negative samples.
Usage ./homework3 -img image path -des output path -output output file name or python homework3.py -img image path -des output path -output output file name

2. Use resize.py to turn the positive sample size to 20*20 and become gray scale.
Usage ./resize -img image path -des destination path or python resize.py -img image path -des destination path

3. Use generate_txt.py to create positive.txt and negative.txt file.
Usage ./generate_txt -img image or python generate_txt.py -img image

4. Use opencv_createsamples to generate the positive.vec file.
-info: input file, the positive.txt
-vec: output file 
-num: the total number of positive samples

opencv_createsamples -info positive.txt -vec positive.vec -num 184502 -w 20 -h 20

5. Use opencv_traincascade for training, the commend:
-numStages: 20
-featureType: LBP, the default type is Haar. So if you want to use Haar, delete the -featureType and change the -data path to ./pos3000neg10000/Haar
-minHitRate: 0.999
-maxFalseAlaemRate: 0.5
-numPos: the number of positive samples
-numNeg: the number of Negative
-w, -h: image width and height

opencv_traincascade -data ./pos3000neg10000/LBP -vec positive.vec -bg neg.txt -numStages 20 -featureType LBP -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 1000 -numNeg 3000 -w 20 -h 20

6. Use car_detection.py to detect cars.
Usage ./car_detection -img image path -xml xml path -output output path -out_name output image name or python car_detection.py -img image path -xml xml path -output output path -out_name output image name

7. Parking spot analysis application: Use the detected cars to decide if a parking spot is empty.
Usage ./parking_spot -img image path -xml xml path -cascade_xml cascade xml path or python parking_spot.py -img image path -xml xml path -cascade_xml cascade xml path




