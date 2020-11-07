import glob
import cv2 as cv
import numpy as np
from screeninfo import get_monitors
import os


def blur_underlay(img, bkgd_xdim, bkgd_ydim, blur_level=70):

    """
    A function for resizing and blurring an image, then overlaying the original untransformed image in the centre.

    img: opencv2 image object
        image for blurring
    bkgd_xdim: int
        desired x dimension for output
    bkgd_ydim: int
        desired y dimension for output
    blur_level: int
        strength of blur (default: 70)
    """

    img_ratio = img.shape[1] / img.shape[0]

    # Calculate size of foreground image
    bkgd_ratio = bkgd_xdim / bkgd_ydim
    if bkgd_ratio > img_ratio:
        img_x_dim = int((img_ratio * bkgd_ydim))
        img_y_dim = bkgd_ydim
    elif xy_ratio < img_ratio:
        img_x_dim = bkgd_xdim
        img_y_dim = int((bkgd_xdim / img_ratio))
    elif xy_ratio == img_ratio:
        img_x_dim = bkgd_xdim
        img_y_dim = bkgd_ydim

    # Resize foreground image
    if img_y_dim < img.shape[0]:
        img_dim = (img_x_dim, img_y_dim)
        img_resize = cv.resize(img, img_dim)
    elif img_y_dim >= img.shape[0]:
        img_resize = img

    # Resize and blur background image
    bkgd = cv.resize(img, (bkgd_xdim, bkgd_ydim))
    bkgd_blur = cv.GaussianBlur(bkgd, ksize=(0, 0), sigmaX=blur_level)

    # Overlay centred foreground image over background image
    y_offset = int((bkgd_blur.shape[0] - img_resize.shape[0]) / 2)
    x_offset = int((bkgd_blur.shape[1] - img_resize.shape[1]) / 2)
    bkgd_blur[
        y_offset : y_offset + img_resize.shape[0],
        x_offset : x_offset + img_resize.shape[1],
    ] = img_resize

    return bkgd_blur


def wallpaper(
    input_path=f"{os.getcwd()}/raw_images/",
    output_path=f"{os.getcwd()}/processed_images/",
    monitor_num=0,
    filetype=".jpg",
    overwrite=False,
):

    """
    A function to iterate over a directory creating resized and blurred desktop wallpapers from images.

    input_path: str
        path to input images (default: CurrentWorkingDirectory/raw_images/)
    output_path: str
        save path for outputs (default: CurrentWorkingDirectory/processed_images/)
    monitor_num: int
        number monitor to fetch resolution from (default: 0 (primary monitor))
    filetype: str
        input filetype (default: .jpg)
    overwrite: bool
        overwrite images already processed (default: False)
    """

    # Fetch desktop resolution
    m = get_monitors()
    monitor_x_dim = m[monitor_num].width
    monitor_y_dim = m[monitor_num].height

    # Iterate over directory
    for input_image_path in glob.iglob(f"{input_path}*{filetype}"):

        image_name = os.path.basename(input_image_path)
        output_image_path = f"{output_path}blurpaper_{image_name}"

        # Skip already processed files
        if (os.path.exists(output_image_path) == True) & ~overwrite:
            print(f"{image_name} already processed")
            continue

        # Load image and transform
        img = cv.imread(input_image_path, 1)
        bkgd_blur = blur_underlay(
            img=img, bkgd_xdim=monitor_x_dim, bkgd_ydim=monitor_y_dim
        )

        # Write file
        print(f"Image saved to {output_image_path}")
        cv.imwrite(output_image_path, bkgd_blur)

    print("Done!")