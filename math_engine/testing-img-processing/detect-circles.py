#from: 
#https://www.geeksforgeeks.org/circle-detection-using-opencv-python/
#https://stackoverflow.com/questions/16615662/how-to-write-text-on-a-image-in-windows-using-python-opencv2

import cv2 
import numpy as np 

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (0,255,255)
thickness              = 1
lineType               = 2

def get_corner_circles(detected_circles):
    closest = []
    
    return closest

# Read image. 
img = cv2.imread("C:\\Users\\Jenny\\Documents\\WallBoundProjector\\math-engine\\right-tilt-circles.png", cv2.IMREAD_COLOR) 
  
# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 

DP = 1
MINDIST = 50

# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(
                    image = gray_blurred,  
                    method = cv2.HOUGH_GRADIENT, 
                    dp = DP, 
                    minDist= MINDIST, 
                    param1 = 50, #higher than param2. 
                    param2 = 30,  #how perfect circles are
                    minRadius = 5,
                    maxRadius = 25) 
# Draw circles that are detected. 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    #find 4 circles in closest size? and 
    #some posters could have circles too

    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
  
        #radius size
        cv2.putText(img,
            str(r), 
            (a,b), 
            font, 
            fontScale,
            fontColor,
            thickness,
            lineType)
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 


    #get 4 sorta equidist from the origin that are similar in size
    
    corner_circles = get_corner_circles(detected_circles)

    cv2.imshow("Detected Circle", img) 
    cv2.waitKey(0) 