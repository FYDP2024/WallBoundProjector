#transformations
# 1. nodding (accelerometer y axis) pitch 
# 2. huh? head rotating (acceleroemter x axis) roll 
# 3. left right (image processing) yaw ********
# 4. zoom and crop ?
import cv2
import shared_transform
import detect_center_circle
import math

#find corners and make them into proper rectangle
#get the matrix of that transformation and remove the roll, pitch, zoom

YAW_FOLDER = shared_transform.CURRENT_FOLDER + "\\yaw_imgs\\"
def yaw_transform(img_path = YAW_FOLDER + "dumb.jpg"):

    #z_degrees = detect_center_circle.calculate_yaw()
    z_degrees = get_yaw_by_distances(1.5,2)
    unskewed_image = shared_transform.read_img(img_path)
    M = shared_transform.get_yaw_z_transform_matrix(z_degrees, unskewed_image.shape)
    yaw_img = cv2.warpPerspective(unskewed_image, M, (unskewed_image.shape[0], unskewed_image.shape[1]))

    shared_transform.display_img("Original", unskewed_image)
    shared_transform.display_img("Yawed", yaw_img)
    
    #save image
    save_path = YAW_FOLDER + "yaw_final.png"
    # cv2.imwrite(
    #     save_path,
    #     yaw_img,
    # )
    return save_path
DEGREES_BETWEEN_SENSORS = 30
def get_yaw_by_distances(d_left, d_right):
    d_wall = math.sqrt(d_left**2 + d_right**2 - 2*d_right*d_left*math.cos(math.radians(DEGREES_BETWEEN_SENSORS)))
    beta = math.acos((d_wall**2 + d_right**2 - d_left**2) / (2*d_wall*d_right))
    yaw_angle = math.radians(DEGREES_BETWEEN_SENSORS/2) + beta - math.pi/2
    return -1*math.degrees(yaw_angle)

    

def main():
    yaw_transform()

if __name__ == '__main__':
    main()