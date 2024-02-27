import cv2
import pathlib
import numpy as np


CURRENT_FOLDER = str(pathlib.Path(__file__).parent.resolve())

def read_img(path):
    img = cv2.imread(path)
    
    if img is None: 
        msg = f"img for not found at {path}"
        raise Exception(msg)
    else: 
        return img
    

def display_img(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)

#zoom and roll
def warpAffine(img, zoom = 1, angle = 0, coord=None):
    cy, cx = [i / 2 for i in img.shape[:-1]] if coord is None else coord[::-1]

    rot_mat = cv2.getRotationMatrix2D((cx, cy), angle, zoom)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)

    return result

#return matrix for transformation based on input in degrees
#edit input degrees so that the transformation is correct (not so sensitive?)
def get_yaw_z_transform_matrix(z_degrees,shape):
    theta_rad = np.deg2rad(z_degrees/100)
    print(theta_rad)
    R = np.array([[np.cos(theta_rad),  0, np.sin(theta_rad)],
                  [0,                  1, 0],
                  [-np.sin(theta_rad), 0, np.cos(theta_rad)]])
    return center_matrix_transform(R, shape)

def get_roll_x_transform_matrix(x_degrees,shape): #roll, normal input
    psi_rad = np.deg2rad(x_degrees)
    R = np.array([[np.cos(psi_rad), -np.sin(psi_rad), 0],
                  [np.sin(psi_rad),  np.cos(psi_rad), 0],
                  [0,                0,               1]])
    return center_matrix_transform(R, shape)

def get_pitch_y_transform_matrix(y_degrees,shape):

    phi_rad = np.deg2rad(y_degrees)
    R = np.float32([[1, 0,                0],
                  [0, np.cos(phi_rad), -np.sin(phi_rad)],
                  [0, np.sin(phi_rad),  np.cos(phi_rad)]])
    return center_matrix_transform(R, shape)

def center_matrix_transform(M, shape):
    M_translate = np.float32([[1,0,-shape[0]//2],[0,1,-shape[1]//2], [0,0,1]])
    M_translate_inv = np.float32([[1,0,shape[0]//2],[0,1,shape[1]//2], [0,0,1]])
    return M_translate_inv.dot(M.dot(M_translate))