#transformations
# 1. nodding (accelerometer y axis) pitch 
# 2. huh? head rotating (acceleroemter x axis) roll 
# 3. left right (image processing) yaw ********
# 4. zoom and crop ?
import cv2
import math_engine.shared_transform as sharedtransform
import math

YAW_FOLDER = sharedtransform.CURRENT_FOLDER + "\\yaw_imgs\\"
def yaw_transform(d_left, d_center, input_image):

    z_degrees = get_yaw_by_distances(d_left, d_center)
    unskewed_image = input_image
    M = sharedtransform.get_yaw_z_transform_matrix(z_degrees, unskewed_image.shape)
    yaw_img = cv2.warpPerspective(unskewed_image, M, (unskewed_image.shape[0], unskewed_image.shape[1]))

    #shared_transform.display_img("Original", unskewed_image)
    #shared_transform.display_img("Yawed", yaw_img)
    return yaw_img
    #save image
    save_path = YAW_FOLDER + "yaw_final.png"
    cv2.imwrite(
        save_path,
        yaw_img,
    )
    

DEGREES_BETWEEN_SENSORS = 15
def get_yaw_by_distances(d_left, d_center):
    d_wall = math.sqrt(d_left**2 + d_center**2 - 2*d_center*d_left*math.cos(math.radians(DEGREES_BETWEEN_SENSORS)))
    beta = math.acos((d_wall**2 + d_center**2 - d_left**2) / (2*d_wall*d_center))
    yaw_angle =  beta - math.pi/2
    #print(math.degrees(yaw_angle))
    return math.degrees(yaw_angle)/150

    

def main():
    yaw_transform()

if __name__ == '__main__':
    main()