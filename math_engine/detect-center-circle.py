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

CIRCLE_DIAMETER_M = 0.1
YAW_FOLDER = shared_transform.CURRENT_FOLDER + "\\yaw_imgs\\"
PICAM_IMG_PATH = YAW_FOLDER + "green_right.png"

def get_corner_circles(img_path = PICAM_IMG_PATH):
    #load picam image
    picam_img = shared_transform.read_img(img_path)
    
    # OPTION: get green circles
    # green_low = np.array([0,0,0])
    # green_high = np.array([200,255,200])    
    # mask = cv2.inRange(picam_img, green_low, green_high)
    # cv2.imshow("green?", mask)
    # cv2.waitKey(0)
    
    # OPTION: Convert to grayscale. 
    gray = cv2.cvtColor(picam_img, cv2.COLOR_BGR2GRAY) 
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    #denoise
    denoised = cv2.bilateralFilter(gray_blurred,9,75,75)
    #cv2.imshow("denoise",denoised)
    #cv2.waitKey(0)


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
        #sort by radius
        sorted_indices = np.argsort(detected_circles[0][:, 2])
        sorted_raw_circles = detected_circles[0][sorted_indices]

        # Use the sorted indices to reorder the array
        circles = np.uint16(np.around(detected_circles))[0]
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

        #cv2.imshow("Detected Circle", picam_img) 
        #cv2.waitKey(0) 
        return sorted_raw_circles[closest_index:closest_index+4]
    else:
        print("I DIDNT DETECT ANY CIRCLES T_T")
        return []
WORLD_COORDS = [(450,250),(450,165),(550,250),(550,165)]
def calculate_yaw():
    circle_coords = np.delete(get_corner_circles(),2,1)
    sorted_indices = np.lexsort((circle_coords[:, 1], circle_coords[:, 0]))
    sorted_circle_coords = circle_coords[sorted_indices]
    print(sorted_circle_coords)
    # Assuming circle_coords is a list of (x, y) coordinates of detected circles
    # and world_coords is a list of corresponding 3D world coordinates

    # Convert to NumPy arrays
    world_coords = np.array(WORLD_COORDS, dtype=np.float32)

    # Add a homogeneous coordinate (1) to 2D coordinates
    homogeneous_circle_coords = np.column_stack((circle_coords, np.ones(circle_coords.shape[0])))

    # Create the linear system (AX = 0)
    A = np.zeros((8, 9))
    for i in range(4):
        A[2*i, :3] = -world_coords[i, :]
        A[2*i, 6:] = world_coords[i, :] * homogeneous_circle_coords[i, 0]
        A[2*i + 1, 3:6] = -world_coords[i, :]
        A[2*i + 1, 6:] = world_coords[i, :] * homogeneous_circle_coords[i, 1]

    # Solve the linear system
    _, _, V = cv2.SVDecomp(A)
    H = V[-1, :].reshape((3, 3))

    # Factorize H into K and R
    K, R = cv2.RQ(H)

    # Normalize K to have a positive focal length
    if K[0, 0] < 0:
        K = -K
        R = -R

    # Extract yaw angle
    yaw = np.arctan2(R[1, 0], R[0, 0])

    # Print the yaw angle in degrees
    print("Yaw Angle: ", np.degrees(yaw))

def main():
    calculate_yaw()

if __name__ == '__main__':
    main()