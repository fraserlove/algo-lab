'''
Image Background Extender
Author: Fraser Love, me@fraser.love
Created: 2024-09-30
Latest Release: v1.0.0, 2024-09-30
Python: v3.10.12
Dependencies: pillow

Extends the background of an image to a desired size, copying the border pixels of the original image to the new edges.
'''

from PIL import Image

def extend_image(input_path, output_path, extension_size):
    # Open the image
    image = Image.open(input_path)
    
    # Get the size of the original image
    width, height = image.size
    
    # Create a new image with extended size
    extended_image = Image.new(image.mode, (width + 2*extension_size, height + 2*extension_size))
    
    # Paste the original image in the center of the new image
    extended_image.paste(image, (extension_size, extension_size))
    
    # Extend the left and right edges
    for y in range(height):
        left_pixel = image.getpixel((0, y))
        right_pixel = image.getpixel((width - 1, y))
        for x in range(extension_size):
            extended_image.putpixel((x, y + extension_size), left_pixel)
            extended_image.putpixel((width + extension_size + x, y + extension_size), right_pixel)
    
    # Extend the top and bottom edges
    for x in range(width + 2*extension_size):
        top_pixel = extended_image.getpixel((x, extension_size))
        bottom_pixel = extended_image.getpixel((x, height + extension_size - 1))
        for y in range(extension_size):
            extended_image.putpixel((x, y), top_pixel)
            extended_image.putpixel((x, height + extension_size + y), bottom_pixel)
    
    # Save the extended image
    extended_image.save(output_path, quality=100)
    return extended_image

input_image_path = 'input.jpg'
output_image_path = 'output.jpg'
extension_size = 250

extended_image = extend_image(input_image_path, output_image_path, extension_size)