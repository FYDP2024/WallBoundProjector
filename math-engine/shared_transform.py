import cv2
import pathlib


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