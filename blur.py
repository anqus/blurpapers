import glob
import cv2 as cv
import numpy as np
from screeninfo import get_monitors
import os

def blur_underlay(
    img, 
    x_dim=0, 
    y_dim=0, 
    blur_level=70
    ):

    if x_dim==0:
        x_dim = img.shape[1]
    if y_dim==0:
        y_dim = img.shape[0]

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
    y_offset = int((bkgd_blur.shape[0]-img_resize.shape[0])/2)
    x_offset = int((bkgd_blur.shape[1]-img_resize.shape[1])/2)
    bkgd_blur[
        y_offset:y_offset+img_resize.shape[0], 
        x_offset:x_offset+img_resize.shape[1]] = img_resize

    return bkgd_blur


def wallpaper(
    input_path=f'{os.getcwd()}/raw_images/', 
    output_path=f'{os.getcwd()}/processed_images/', 
    monitor_num=0, 
    filetype='.jpg'
    ):

    # Fetch desktop resolution
    m = get_monitors()
    monitor_x_dim=m[monitor_num].width
    monitor_y_dim=m[monitor_num].height

    for input_image_path in glob.iglob(f'{input_path}*{filetype}'):

        image_name = os.path.basename(input_image_path)
        output_image_path = f'{output_path}blurpaper_{image_name}'       
        if os.path.exists(output_image_path) == True:
            print(f'{image_name} already processed')
            continue

        # Load image and transform
        img = cv.imread(input_image_path, 1)
        bkgd_blur = blur_underlay(
            img, 
            x_dim=monitor_x_dim, 
            y_dim=monitor_y_dim
            )

        # Write file
        print(output_image_path)
        cv.imwrite(output_image_path,bkgd_blur)

    print('Done!')
