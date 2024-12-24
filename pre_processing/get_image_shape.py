'''


check the size of the image

'''

from PIL import Image

# Open the image
img = Image.open('image path')


# Get image dimensions
width, height = img.size
print(f"Image width: {width}, height: {height}")


# 1170 - 2532

