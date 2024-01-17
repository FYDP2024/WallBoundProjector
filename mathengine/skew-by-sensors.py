#transformations
# 1. zoom
# 2. nodding (accelerometer y axis)
# 3. huh? head rotating (acceleroemter x axis)
# 4. left right (image processing)
# 5. crop ?


 #getRotationMatrix can do distance and rotation in x axis of accelerometer

import cv2

PROJECTOR_RESOLUTION_HEIGHT = 1080
PROJECTOR_RESOLUTION_WIDTH = 1920

THROW_RATIO = 88/120 #converts distance to width of projector
INPUT_IMAGE_DIMENSIONS_IRL = (4,4) #in meters (h,w)

#input distance in meters
def distance_transform(distance):
    unskewed_image_path = "C:\\Users\\shiji\\OneDrive\\Documents\\4B\ECE498B\\WallBoundProjector\\mathengine\\square_bg.png"
    unskewed_image = cv2.imread(unskewed_image_path) 

    curr_projection_width_m = distance * THROW_RATIO #width of projection in meters

    pixels_per_m = PROJECTOR_RESOLUTION_WIDTH / curr_projection_width_m

    # note: shape[1] is width of image
    curr_image_size_m = unskewed_image.shape[1] / pixels_per_m
    zoom = INPUT_IMAGE_DIMENSIONS_IRL[1] / curr_image_size_m

    zoomed_image = zoom_at(unskewed_image, zoom)

    #show image
    cv2.imshow("Original", unskewed_image)
    cv2.imshow("user", zoomed_image)
    cv2.waitKey(0)

    #save image
    cv2.imwrite(
        "C:\\Users\\shiji\\OneDrive\\Documents\\4B\\ECE498B\\WallBoundProjector\\mathengine\\zoomed.png",
        zoomed_image,
    )
    return zoomed_image

def zoom_at(img, zoom = 1, angle = 0, coord=None):

    cy, cx = [i / 2 for i in img.shape[:-1]] if coord is None else coord[::-1]

   
    rot_mat = cv2.getRotationMatrix2D((cx, cy), angle, zoom)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)

    return result

def pad_image(img):
    height_padding = (PROJECTOR_RESOLUTION_HEIGHT - img.size[0]) // 2
    width_padding = (PROJECTOR_RESOLUTION_WIDTH - img.size[1]) // 2

    height_padding = max(height_padding, 0)
    width_padding = max(width_padding, 0)

    return cv2.copyMakeBorder(img, height_padding, height_padding, width_padding, width_padding, cv2.BORDER_CONSTANT, [255,255,255,0])
distance_transform(2.45)