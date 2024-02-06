import cv2

#from: https://dontrepeatyourself.org/post/edge-and-contour-detection-with-opencv-and-python/

#simplifies image to lines
#can potentially use those lines to determine skew
#but there will be poster images on the wall, can confuse the image

image = cv2.imread("C:\\Users\\Jenny\\Documents\\WallBoundProjector\\math-engine\\right-tilt.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

edged = cv2.Canny(blurred, 10, 100)

cv2.imshow("Original image", image)
cv2.imshow("Edged image", edged)
cv2.waitKey(0)