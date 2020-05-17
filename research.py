import cv2 as cv
import numpy as np
from screeninfo import get_monitors

# User defined input variables
monitor_num = 0
blur_level = 40
input_path='images/'
output_path='blurpapers/'
image_name='2'
filetype='.jpg'

# Derived input variables
m = get_monitors()
x_dim=m[monitor_num].width
y_dim=m[monitor_num].height
input_image_path= f'{input_path}{image_name}{filetype}'
output_image_path= f'{output_path}blurpaper_{image_name}{filetype}'
xy_dim = (x_dim, y_dim)
xy_ratio=x_dim/y_dim

# Load image/ aspect ratio
img = cv.imread(input_image_path, 1)
img_ratio = img.shape[1]/img.shape[0]

# Calculate size of foreground image
if xy_ratio>img_ratio:
    img_x_dim = int((img_ratio*y_dim))
    img_y_dim = y_dim
elif xy_ratio<img_ratio:
    img_x_dim = x_dim
    img_y_dim = int((x_dim/img_ratio))
elif xy_ratio==img_ratio:
    img_x_dim = x_dim
    img_y_dim = y_dim

# Resize foreground image
if img_y_dim<img.shape[0]:
    img_dim = (img_x_dim ,img_y_dim)
    img_resize = cv.resize(img, img_dim)
elif img_y_dim>=img.shape[0]:
    img_resize = img

# Resize and blur background image
bkgd = cv.resize(img, xy_dim)
bkgd_blur = cv.GaussianBlur(bkgd,ksize=(0,0),sigmaX=blur_level)

# Overlay centred foreground image over background image
y_offset=int((bkgd_blur.shape[0]-img_resize.shape[0])/2)
x_offset=int((bkgd_blur.shape[1]-img_resize.shape[1])/2)
bkgd_blur[y_offset:y_offset+img_resize.shape[0], x_offset:x_offset+img_resize.shape[1]] = img_resize

