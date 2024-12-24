'''
combine single input image side by side for visualization

'''


import os
import cv2
import numpy as np

def combine_single_image(light_image_file, dark_image_file, output_image_path):
    # Check if both images exist
    if not os.path.exists(light_image_file):
        print(f"Light mode image missing: {light_image_file}")
        return
    if not os.path.exists(dark_image_file):
        print(f"Dark mode image missing: {dark_image_file}")
        return

    # Load the images
    image1 = cv2.imread(light_image_file)
    image2 = cv2.imread(dark_image_file)

    if image1 is None or image2 is None:
        print(f"Error loading images: {light_image_file} or {dark_image_file}")
        return

    # # for the application that support both light and dark mode
    # Concatenate images horizontally
    side_by_side = np.hstack((image1, image2))

    # # for application that only support dark mode and used extension to convert into the light mode
    # # Concatenate images horizontally
    # side_by_side = np.hstack((image2, image1))

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

    # Save the combined image
    cv2.imwrite(output_image_path, side_by_side)
    print(f"Saved combined image: {output_image_path}")

    ### Optionally display the combined image
    # cv2.imshow('Side by Side Images', side_by_side)
    # cv2.waitKey(0)  # Wait for a key press
    # cv2.destroyAllWindows()

    return output_image_path  # Return the path of the saved image

# Define the file paths
light_image_file = 'path/to/light screenshot'
dark_image_file = 'path/tp/dark screenshot'
output_image_path = 'path/to/output directory'

# Run the function for a single image
combined_image = combine_single_image(light_image_file, dark_image_file, output_image_path)
print("Result:", combined_image)
