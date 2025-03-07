'''
Transparent Background
Author: Fraser Love, me@fraser.love
Created: 2025-03-06
Latest Release: v1.0.0, 2025-03-06
Python: v3.10.12
Dependencies: pillow

Removes drop shadow from an image, making it transparent and cropping the image to the non-transparent areas.
'''

from PIL import Image

def make_transparent_and_crop(input_path, output_path, border=0):
    # Open the image
    img = Image.open(input_path).convert("RGBA")
    
    # Get the image data
    pixels = img.getdata()
    
    # Modify pixels: make only black and partially transparent pixels fully transparent
    new_pixels = [(r, g, b, 0) if a < 255 and r == 0 and g == 0 and b == 0 else (r, g, b, a) for r, g, b, a in pixels]
    
    # Update image data
    img.putdata(new_pixels)
    
    # Auto-crop transparent areas
    bbox = img.getbbox()
    if bbox:
        left, upper, right, lower = bbox
        left = max(0, left - border)
        upper = max(0, upper - border)
        right = min(img.width, right + border)
        lower = min(img.height, lower + border)
        img = img.crop((left, upper, right, lower))
    
    # Save the modified image
    img.save(output_path, "PNG")

# Example usage
input_file = "assets/example.png"   # Replace with your input file
output_file = "assets/example_transparent.png" # Replace with your desired output file
make_transparent_and_crop(input_file, output_file)