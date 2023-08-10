'''
Image Resizer
Author: Fraser Love, me@fraser.love
Created: 2020-06-21
Latest Release: v1.0.0, 2020-06-21
Python: v3.10.12
Dependencies: pillow

Resizes images to a desired width and/or height and can optionally maintain the images aspect ratio. The images can 
be converted to another file type if chosen.

Usage:  Update the img_dir and new_img_dir paths to point to the directory that holds the image files and the directory 
        that the newly generated images should be placed under. Set maintain_aspect_ratio depending on if the images 
        individual aspect ratios should be maintained or not. If maintaining aspect ratio only new_width or new_height 
        needs to be assigned to an integer, otherwise both values should be set. Set maintain_file_type to the desired 
        value. If images should be converted to a new file type then set the new_file_type variable to the appropriate 
        image file extension.
'''

from PIL import Image
import os

img_dir = 'images/' # Include trailing forward slash
new_img_dir = 'new-images/'
maintain_aspect_ratio = True # Images are scaled to some width or height and maintain the same aspect ratio
maintain_file_type = True # New images are given the same file type as the original images

new_width = 400 # In pixels
new_height = None
new_file_type = '.png' # Image extension for chosen format *.png, *.jpg, *.gif

if maintain_aspect_ratio:
    if new_height != None and new_width != None:
        print('ERROR: Aspect ratio cannot be maintained while new_width and new_height are both set.')

if new_height == None and new_width == None:
    if not maintain_aspect_ratio:
        print('ERROR: A new_width and new_height for the images has to be set.')
    else:
        print('ERROR: A new_width or new_height for the images has to be set in order to maintain aspect ratio.')

img_names = [img_name for img_name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, img_name))]

for img_name in img_names:
    img = Image.open('{}{}'.format(img_dir, img_name))
    
    width, height = img.size
    aspect_ratio = width / height
    if maintain_aspect_ratio:
        if new_height == None:
            img_height = int(new_width / aspect_ratio)
            img_width = new_width
        elif new_width == None:
            img_width = int(new_height * aspect_ratio)
            img_height = new_height

    img = img.resize((img_width, img_height), Image.ANTIALIAS)

    directory = '{}'.format(new_img_dir)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not maintain_file_type:
        img_name = img_name.split('.')[0] + new_file_type

    img.save('{}{}'.format(new_img_dir, img_name))