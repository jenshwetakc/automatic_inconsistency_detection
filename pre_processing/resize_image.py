'''


resize the original screenshot into the uied size

'''

import cv2
import os


input_folder = "path to image"
output_folder = "output path"  # Folder to save results

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # Add more extensions if needed
        # Read the image
        image_path = os.path.join(input_folder, filename)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at path:{image_path}")
        image = cv2.imread(image_path)

        # Resize the image to 500x700 pixelss
        resized_image = cv2.resize(image, (369, 800))
        # resized_image = cv2.resize(image, (1170, 2532)) - test
        # uied web
        # resized_image = cv2.resize(image, (799, 553))

        # Save the resized image in the output folder
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, resized_image)

        print(f'Resized and saved: {output_path}')

print("Resizing complete.")

'''
note: 
mega uied size: 369, 800
'''