# takes all measurements outputs skewed input image
# roll, pitch, yaw zoom
import cv2
import math_engine.shared_transform as sharedtransform
import math_engine.transform_config as transform_config
import math
from math_engine.transform_config import transform_config

ZOOM_FOLDER = sharedtransform.CURRENT_FOLDER + "/zoom_imgs/"
def all_transforms(input_image, roll_degrees, pitch_degrees, distance, yaw_distance, config: transform_config):
    yaw_degrees = get_yaw_by_distances(yaw_distance, distance, config.degrees_between_dist_sensors)

    # correct distance by yaw angle
    #distance = distance * math.cos(math.radians(yaw_degrees))
    
    x_degrees = roll_degrees - config.roll_offset
    y_degrees = (pitch_degrees - config.pitch_offset)*config.pitch_scale_factor
    z_degrees = yaw_degrees*config.yaw_scale_factor

    M_roll = sharedtransform.get_roll_x_transform_matrix(x_degrees, input_image.shape)
    M_pitch = sharedtransform.get_pitch_y_transform_matrix(y_degrees, input_image.shape)
    M_yaw = sharedtransform.get_yaw_z_transform_matrix(z_degrees, input_image.shape)

    M = M_roll.dot(M_pitch).dot(M_yaw)
    skewed_img = cv2.warpPerspective(input_image, M, (input_image.shape[0], input_image.shape[1]))

    if distance == 0:
        print("Distance is 0 error")
        distance = 100

    if skewed_img.shape[0] < config.input_image_dimension_px[0]: #paste onto transparent background if img is smaller than 4k
        transparent_bg = cv2.imread(ZOOM_FOLDER + "4kbg.png")

        x_offset = (transparent_bg.shape[1] - skewed_img.shape[1]) // 2
        y_offset = (transparent_bg.shape[0] - skewed_img.shape[0]) // 2

        transparent_bg[
            y_offset : y_offset + skewed_img.shape[0],
            x_offset : x_offset + skewed_img.shape[1],
        ] = skewed_img

        skewed_img = transparent_bg


    curr_projection_width_m = distance * config.throw_ratio #width of projection in meters
    img_px_width_to_show = int(round(curr_projection_width_m * config.input_image_dimension_px[1] / config.input_image_dimension_m[1]))

    projector_height = config.projector_resolution_px[0]
    projector_width = config.projector_resolution_px[1]
    zoom = projector_width / img_px_width_to_show
    zoomed_image = sharedtransform.warpAffine(skewed_img, zoom = zoom)
    
    #crop image to this pixel size
    x = (config.input_image_dimension_px[1] - projector_width)//2
    y = (config.input_image_dimension_px[0] - projector_height)//2
    cropped_final_image = zoomed_image[y:y + projector_height,x:x + projector_width]
    return cropped_final_image


def get_yaw_by_distances(d_left, d_center, degrees_between_dist_sensors):
    d_wall = math.sqrt(d_left**2 + d_center**2 - 2*d_center*d_left*math.cos(math.radians(degrees_between_dist_sensors)))
    beta = math.acos((d_wall**2 + d_center**2 - d_left**2) / (2*d_wall*d_center))
    yaw_angle =  beta - math.pi/2
    return math.degrees(yaw_angle) * -1

def main():
    img = sharedtransform.read_img(ZOOM_FOLDER+"dumb.jpg")

    config = transform_config()
    ret_img = all_transforms(img, 0, 10, 2, 2.07055,config)

    sharedtransform.display_img("test", ret_img)
if __name__ == '__main__':
    main()