#transformations
# 1. nodding (accelerometer y axis) pitch 
# 2. huh? head rotating (acceleroemter x axis) roll ********
# 3. left right (image processing) yaw
# 4. zoom and crop ?

#roll can be done with the function used for zoom

#measure of x rotation in degrees.
#in POV of projector, rotating counter clockwise (left) is positive
import cv2
import shared_transform

ROLL_FOLDER = shared_transform.CURRENT_FOLDER + "\\roll_imgs\\"
def roll_transform(x_degrees):
    #TODO: get image from last transformation
    unskewed_image = shared_transform.read_img(ROLL_FOLDER + "dumb.jpg")

    rolled_img = shared_transform.warpAffine(unskewed_image, angle= x_degrees)

    # shared_transform.display_img("Original",unskewed_image)
    # shared_transform.display_img("Rolled",rolled_img)
    
    #save image
    cv2.imwrite(
        ROLL_FOLDER + "rolled_final.png",
        rolled_img,
    )

#TEST CALL
roll_transform(90)