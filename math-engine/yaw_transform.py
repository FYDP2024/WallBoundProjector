#transformations
# 1. nodding (accelerometer y axis) pitch 
# 2. huh? head rotating (acceleroemter x axis) roll 
# 3. left right (image processing) yaw ********
# 4. zoom and crop ?
import cv2
import shared_transform

YAW_FOLDER = shared_transform.CURRENT_FOLDER + "\\yaw_imgs\\"
def yaw_transform(x_degrees, img_path = YAW_FOLDER + "dumb.jpg"):
    unskewed_image = shared_transform.read_img(img_path)

    M = shared_transform.get_yaw_z_transform_matrix(x_degrees, unskewed_image.shape)
    yaw_img = cv2.warpPerspective(unskewed_image, M, (unskewed_image.shape[0], unskewed_image.shape[1]))

    #shared_transform.display_img("Original",unskewed_image)
    #shared_transform.display_img("Rolled",rolled_img)
    
    #save image
    save_path = YAW_FOLDER + "yaw_final.png"
    cv2.imwrite(
        save_path,
        yaw_img,
    )
    return save_path