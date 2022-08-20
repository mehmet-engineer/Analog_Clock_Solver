import cv2
import numpy as np
import math

img = cv2.imread("clock_1.jpg")
img = cv2.resize(img,(600,600))

# IMAGE PREPROCESSING
imgGRAY = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlurred = cv2.blur(imgGRAY,(4,4))
canny = cv2.Canny(imgBlurred,180,250,apertureSize=3)

lines = cv2.HoughLinesP(canny, rho=2, theta=np.pi/180, threshold=120, minLineLength=10, maxLineGap=12)
print(lines)

angles = []
if lines is not None:
    for line in lines:  
        for x1,y1,x2,y2 in line:
            slope = (y2-y1)/(x2-x1)
            radyan_angle = math.atan(slope)
            angle = round(math.degrees(radyan_angle))
            angles.append(angle)

            if angle > 0:
                cv2.line(img,(x1,y1),(x2,y2),[0,255,0],2)
            else:
                cv2.line(img,(x1,y1),(x2,y2),[0,0,255],2)
print("\n Angles:")
print(angles)

# FINDING ZONES
radius = 20
zone_points = []
center = ( int(img.shape[0]/2), int(img.shape[1]/2) )
cv2.circle(img, center, radius, [255,0,0], 2)
if lines is not None:
    for line in lines:  
        for x1,y1,x2,y2 in line:
            length_1 = math.sqrt( (center[0]-x1)**2 + (center[1]-y1)**2 )
            length_2 = math.sqrt( (center[0]-x2)**2 + (center[1]-y2)**2 )
            if length_1 > length_2:
                zone_points.append((x1,y1))
            else:
                zone_points.append((x2,y2))

#for i in zone_points:
#    cv2.circle(img, i, 5, [255,0,0], 2)

print(zone_points)

zones = []
for x,y in zone_points:
    if (x > center[0]) and (y < center[0]):
        zones.append(1)
    if (x < center[0]) and (y < center[0]):
        zones.append(2)
    if (x < center[0]) and (y > center[0]):
        zones.append(3)
    if (x > center[0]) and (y > center[0]):
        zones.append(4)

print(zones)

distances = []
for line in lines:
    for x1,y1,x2,y2 in line:
        distance = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
        distances.append(int(distance))

print(distances)

data = list(zip(distances,angles,zones))
print("\n data:")
print(data)

print("\n sorted data:")
data.sort()
print(data)

akrep_data = data[:2]
yelkovan_data = data[2:]
print("\n akrep:", akrep_data)
print(" yelkovan:", yelkovan_data)

# DETECT YELKOVAN CLOCK
yelkovan_angle = abs( (yelkovan_data[0][1] + yelkovan_data[1][1]) / 2 )
yelkovan_zone = yelkovan_data[0][2]
# 30 degree --> 5 min
# 1 degree --> 0.16 min
if yelkovan_zone == 1:
    new_angle = 90 - yelkovan_angle
    min = int( new_angle * 0.16 )
    print(min)

# DETECT AKREP CLOCK
akrep_angle = abs( (akrep_data[0][1] + akrep_data[1][1]) / 2 )
akrep_zone = akrep_data[0][2]
# 30 degree --> 1 hours
# 1 degree --> 0.033 hours
if akrep_zone == 2:
    add = int( akrep_angle * 0.033 )
    hour = 9 + add
    print(hour)

if min < 10:
    min = "0" + str(min)
my_string = str(hour) + ":" + min

cv2.putText(img, my_string, (40,550), cv2.FONT_HERSHEY_COMPLEX, 1.5, [0,0,0], 2)


cv2.imshow("original",img)
cv2.waitKey()
cv2.destroyAllWindows()