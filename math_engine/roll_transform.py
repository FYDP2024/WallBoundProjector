#transformations
# 1. nodding (accelerometer y axis) pitch 
# 2. huh? head rotating (acceleroemter x axis) roll ********
# 3. left right (image processing) yaw
# 4. zoom and crop ?

#roll can be done with the function used for zoom

#measure of x rotation in degrees.
#in POV of projector, rotating counter clockwise (left) is positive
import cv2
import math_engine.shared_transform as shared_transform

ROLL_FOLDER = shared_transform.CURRENT_FOLDER + "\\roll_imgs\\"
def roll_transform(x_degrees, input_image):
    unskewed_image = input_image

    M = shared_transform.get_roll_x_transform_matrix(x_degrees, unskewed_image.shape)
    rolled_img = cv2.warpPerspective(unskewed_image, M, (unskewed_image.shape[0], unskewed_image.shape[1]))

    #shared_transform.display_img("Original",unskewed_image)
    #shared_transform.display_img("Rolled",rolled_img)
    return rolled_img
    #save image
    save_path = ROLL_FOLDER + "rolled_final.png"
    cv2.imwrite(
        save_path,
        rolled_img,
    )
    return save_path

#TEST CALL
#roll_transform(45)