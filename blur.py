import glob
import cv2 as cv
import numpy as np
from screeninfo import get_monitors
import ntpath
import pathlib

def blurpaper(x_dim, y_dim, input_image_path, blur_level, output_path):

    image_name=ntpath.basename(input_image_path)
    output_image_path = f'{output_path}blurpaper_{blur_level}_{image_name}'
    path = pathlib.Path(output_image_path)
    if path.exists() == True:
        return

    # Load image/ aspect ratio
    img = cv.imread(input_image_path, 1)
    img_ratio = img.shape[1]/img.shape[0]

    # Calculate size of foreground image
    xy_ratio=x_dim/y_dim
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
    bkgd = cv.resize(img, (x_dim,y_dim))
    bkgd_blur = cv.GaussianBlur(bkgd,ksize=(0,0),sigmaX=blur_level)

    # Overlay centred foreground image over background image
    y_offset=int((bkgd_blur.shape[0]-img_resize.shape[0])/2)
    x_offset=int((bkgd_blur.shape[1]-img_resize.shape[1])/2)
    bkgd_blur[y_offset:y_offset+img_resize.shape[0], x_offset:x_offset+img_resize.shape[1]] = img_resize

    # Write file
    cv.imwrite(output_image_path,bkgd_blur)

# User defined input variables
monitor_num=0
blur_level=70
input_path='C:/Users/liv3r/OneDrive/Pictures/Favourites/Unedited/'
filetype='.jpg'
output_path='blurpapers/'

# Fetch desktop resolution
m = get_monitors()
x_dim=m[monitor_num].width
y_dim=m[monitor_num].height

for input_image_path in glob.iglob(f'{input_path}*{filetype}'):
    blurpaper(x_dim, y_dim, input_image_path, blur_level, output_path)

print('Done!')