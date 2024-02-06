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
    #data=data[np.argsort(data[:,col])]
    #sorted_dc = sorted(detected_circles[0], reverse= True, key= lambda x:x[2])
    print(detected_circles)
    sorted_dc = detected_circles[detected_circles[:,2].argsort()]
    size = len(sorted_dc)
    max_diff = sorted_dc[0][2] - sorted_dc[-1][2]
    print(max_diff)
    dp = np.zeros((size,size))

    for i in range(size-1):
        for j in range(i+1,min(i+4,size)):
            print(f"{i} {j}")
            dp[i][j] = sorted_dc[i][2] - sorted_dc[j][2] #the difference

    print(dp)

    
    closest = []
    return closest
# Read image. 
img = cv2.imread("C:\\Users\\shiji\\OneDrive\\Documents\\4B\\ECE498B\\WallBoundProjector\\math-engine\yaw_imgs\\straight-on-with-center-cirlce.jpg", cv2.IMREAD_COLOR) 
  
# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
# cv2.imshow("gray", gray)
# cv2.waitKey(0) 

# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 
# cv2.imshow("gray_blurred", gray_blurred)
# cv2.waitKey(0) 

#denoise
denoised = cv2.bilateralFilter(gray_blurred,9,75,75)
# cv2.imshow("denoised", denoised)
# cv2.waitKey(0) 

DP = 1
MINDIST = 50

# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(
                    image = denoised,  
                    method = cv2.HOUGH_GRADIENT, 
                    dp = DP, 
                    minDist= MINDIST, 
                    param1 = 50, #higher than param2. 
                    param2 = 15,  #how perfect circles are
                    minRadius = 20,
                    maxRadius = 40) 

# Draw circles that are detected. 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    #get the four corner circles
   # detected_circles = get_corner_circles(detected_circles[0])
    
    for pt in detected_circles: 
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

    cv2.imshow("Detected Circle", img) 
    cv2.waitKey(0) 

