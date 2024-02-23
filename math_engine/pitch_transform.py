#transformations
# 1. nodding (accelerometer y axis) pitch ********
# 2. huh? head rotating (acceleroemter x axis) roll 
# 3. left right (image processing) yaw
# 4. zoom and crop ?

#looking at cv2.warpperspective

import cv2
import numpy as np
import math_engine.shared_transform as shared_transform

PITCH_FOLDER = shared_transform.CURRENT_FOLDER + "\\pitch_imgs\\"


#rotation in y axis, looking down is negative, looking up is positive

def pitch_transform(y_degrees, input_image):
    unskewed_image = input_image

    M = shared_transform.get_pitch_y_transform_matrix(y_degrees, unskewed_image.shape)
    
    pitched_img = cv2.warpPerspective(unskewed_image, M, (unskewed_image.shape[0], unskewed_image.shape[1]))

    #shared_transform.display_img("Original",unskewed_image)
    #shared_transform.display_img("Pitched",pitched_img)

    return pitched_img
    
    #save image
    save_path = PITCH_FOLDER + "pitched_final.png"
    cv2.imwrite(
        save_path,
        pitched_img,
    )
    return save_path

#TEST CALL
#pitch_transform(10) 
