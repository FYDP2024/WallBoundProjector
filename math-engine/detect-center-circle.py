#detect all circles
#take distance measure
#look for circles at most like 18 degrees away left and right
#uhhh the circle size should be around some size
#closest one to the middle
#look for best circle and treat that as the center
#calculate distance from center and get yaw measurement from it 

import shared_transform
import cv2 
import numpy as np 

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (0,255,255)
thickness              = 1
lineType               = 2

class Circle:
    def __init__(self,a,b,r):
        self.radius = r
        self.coords = (a,b)
        self.dist_from_center = 0
        self.av_colour = None
    
    def find_dist_from_center(self,c_x, c_y):
        a,b = self.coords
        self.dist_from_center = ()


CIRCLE_DIAMETER_M = 0.1
YAW_FOLDER = shared_transform.CURRENT_FOLDER + "\\yaw_imgs\\"
PICAM_IMG_PATH = YAW_FOLDER + "straight-on-with-center-circle.jpg"

def get_yaw_measurement(distance_m,img_path):
    #load picam image
    picam_img = shared_transform.read_img(YAW_FOLDER+img_path)
    
    #get green circles
                #r,g,b
    green_low = np.array([0,0,0])
    green_high = np.array([200,255,200])    
    # mask = cv2.inRange(picam_img, green_low, green_high)
    # cv2.imshow("green?", mask)
    # cv2.waitKey(0)
    
    # Convert to grayscale. 
    gray = cv2.cvtColor(picam_img, cv2.COLOR_BGR2GRAY) 
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    #denoise
    denoised = cv2.bilateralFilter(gray_blurred,9,75,75)
    cv2.imshow("denoise",denoised)
    cv2.waitKey(0)
    DP = 1
    MINDIST = 50

    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(
                        image = denoised,  
                        method = cv2.HOUGH_GRADIENT, 
                        dp = DP, 
                        minDist= MINDIST, 
                        param1 = 50, #higher than param2. 
                        param2 = 20,  #how perfect circles are NOTE: decrease when chroma key
                        minRadius = 5,
                        maxRadius = 20) 

    # Draw circles that are detected. 
    if detected_circles is not None: 
        circles = np.uint16(np.around(detected_circles))[0]

        #sort by radius
        sorted_indices = np.argsort(circles[:, 2])
        # Use the sorted indices to reorder the array
        sorted_circles = circles[sorted_indices]
        #find the circle closest to center

        for i in circles:
            a, b, r = i[0],i[1],i[2]
            cv2.circle(picam_img, (a, b), r, (0, 255, 0), 2)

        

        #get circles that are closest in size?
        if len(circles) < 4:  
            print("didn't even find 4 circles")
            return
        
        closest_index = 0
        closest_size = -1
        for i in range(len(sorted_circles)-3):
            radius_range = sorted_circles[i+3][2] - sorted_circles[i][2]
            if closest_size == -1 or closest_size > radius_range:
                closest_size = radius_range
                closest_index = i
        corner_circles = sorted_circles[closest_index:closest_index+4]

        for c in corner_circles:
            a, b, r = c[0],c[1],c[2]
            cv2.circle(picam_img, (a, b), r, (0, 255, 0),-1)            
        cv2.imshow("Detected Circle", picam_img) 
        cv2.waitKey(0) 
    else:
        print("I DIDNT DETECT ANY CIRCLES T_T")

def main():
    get_yaw_measurement(4,"green_right.png")
    get_yaw_measurement(4,"green_straight.png")

if __name__ == '__main__':
    main()