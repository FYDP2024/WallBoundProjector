#transformations
# 1. nodding (accelerometer y axis) pitch
# 2. huh? head rotating (acceleroemter x axis) roll 
# 3. left right (image processing) yaw
# 4. zoom and crop *******

import cv2
import math_engine.shared_transform as sharedtransform
PROJECTOR_RESOLUTION_HEIGHT = 1080
PROJECTOR_RESOLUTION_WIDTH = 1920

THROW_RATIO = 88/120 #converts distance to width of projector
INPUT_IMAGE_DIMENSIONS_IRL = (4,4) #in meters (h,w)
SET_INPUT_IMAGE_DIMENSIONS_PX = (2200,2200)
ZOOM_FOLDER = sharedtransform.CURRENT_FOLDER + "/zoom_imgs/"
#input distance in meters and img_path of img to transform
#returns path of saved image
def zoom_transform(distance, input_image):

    #print(distance)
    unskewed_image = input_image
    

    if distance == 0:
        print("Distance is 0 error")
        distance = 100

    if unskewed_image.shape[0] < SET_INPUT_IMAGE_DIMENSIONS_PX[0]: #paste onto transparent background if img is smaller than 4k
        transparent_bg = cv2.imread(ZOOM_FOLDER + "4kbg.png")

        x_offset = (transparent_bg.shape[1] - unskewed_image.shape[1]) // 2
        y_offset = (transparent_bg.shape[0] - unskewed_image.shape[0]) // 2

        transparent_bg[
            y_offset : y_offset + unskewed_image.shape[0],
            x_offset : x_offset + unskewed_image.shape[1],
        ] = unskewed_image

        unskewed_image = transparent_bg


    curr_projection_width_m = distance * THROW_RATIO #width of projection in meters
    img_px_width_to_show = int(round(curr_projection_width_m * SET_INPUT_IMAGE_DIMENSIONS_PX[1] / INPUT_IMAGE_DIMENSIONS_IRL[1]))

    zoom = PROJECTOR_RESOLUTION_WIDTH / img_px_width_to_show
    zoomed_image = sharedtransform.warpAffine(unskewed_image, zoom = zoom)
    
    #crop image to this pixel size
    x = (SET_INPUT_IMAGE_DIMENSIONS_PX[1] - PROJECTOR_RESOLUTION_WIDTH)//2
    y = (SET_INPUT_IMAGE_DIMENSIONS_PX[0] - PROJECTOR_RESOLUTION_HEIGHT)//2
    cropped_final_image = zoomed_image[y:y+PROJECTOR_RESOLUTION_HEIGHT,x:x+PROJECTOR_RESOLUTION_WIDTH]

    #shared_transform.display_img("Original",unskewed_image)
    #shared_transform.display_img("Final",cropped_final_image)

    #rerturn image data
    return cropped_final_image

    #save image
    save_path = ZOOM_FOLDER + "zoomed_final.png"
    cv2.imwrite(
        ZOOM_FOLDER + "zoomed_final.png",
        cropped_final_image,
    )
    
    return save_path

def pad_image(img):
    height_padding = (PROJECTOR_RESOLUTION_HEIGHT - img.size[0]) // 2
    width_padding = (PROJECTOR_RESOLUTION_WIDTH - img.size[1]) // 2

    height_padding = max(height_padding, 0)
    width_padding = max(width_padding, 0)

    return cv2.copyMakeBorder(img, height_padding, height_padding, width_padding, width_padding, cv2.BORDER_CONSTANT, [255,255,255,0])


#TEST CALL
#zoom_transform(1.45)
