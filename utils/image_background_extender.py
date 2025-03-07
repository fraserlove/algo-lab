'''
Image Background Extender
Author: Fraser Love, me@fraser.love
Created: 2024-09-30
Latest Release: v1.1.0, 2024-10-01
Python: v3.10.12
Dependencies: pillow

Extends the background of an image to a desired size, either with transparency or by copying the border pixels of the original image to the new edges.

Usage:
python image_background_extender.py <input_image_path> <output_image_path> <extension_size> [mode]

Modes:
    transparent (default): extends the background with transparency
    copy_edge: extends the background by copying the border pixels of the original image to the new edges
'''

from PIL import Image

def extend_image(input_path, output_path, extension_size, mode='transparent'):
    # Open the image
    image = Image.open(input_path)
    
    # Get the size of the original image
    width, height = image.size
    
    # Create a new image with extended size
    if image.mode == 'RGBA':
        extended_image = Image.new('RGBA', (width + 2*extension_size, height + 2*extension_size), (0, 0, 0, 0))
    else:
        extended_image = Image.new('RGBA', (width + 2*extension_size, height + 2*extension_size), (0, 0, 0, 0))
        image = image.convert('RGBA')
    
    # Paste the original image in the center of the new image
    extended_image.paste(image, (extension_size, extension_size), image)
    
    if mode == 'copy_edge':
        # Copy edge pixels to the extended areas
        for x in range(width):
            for i in range(extension_size):
                extended_image.putpixel((x + extension_size, i), image.getpixel((x, 0)))
                extended_image.putpixel((x + extension_size, height + extension_size + i), image.getpixel((x, height - 1)))
        
        for y in range(height):
            for i in range(extension_size):
                extended_image.putpixel((i, y + extension_size), image.getpixel((0, y)))
                extended_image.putpixel((width + extension_size + i, y + extension_size), image.getpixel((width - 1, y)))
        
        # Fill corners
        for x in range(extension_size):
            for y in range(extension_size):
                extended_image.putpixel((x, y), image.getpixel((0, 0)))
                extended_image.putpixel((width + extension_size + x, y), image.getpixel((width - 1, 0)))
                extended_image.putpixel((x, height + extension_size + y), image.getpixel((0, height - 1)))
                extended_image.putpixel((width + extension_size + x, height + extension_size + y), image.getpixel((width - 1, height - 1)))
    
    # Save the extended image
    if input_path.lower().endswith('.png'):
        extended_image.save(output_path, format='PNG')
    else:
        extended_image = extended_image.convert('RGB')
        extended_image.save(output_path, quality=100)

input_image_path = 'favicon.png'
output_image_path = 'favicon_extended.png'
extension_size = 150

# Example usage
extend_image(input_image_path, output_image_path, extension_size, mode='transparent')