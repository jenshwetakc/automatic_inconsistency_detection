'''
December 9
update the code

combine the light and dark screenshot for easy visualization

'''


import os
import cv2
import numpy as np

def get_image_side_by_side(image_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    results = []  # Store results for the batch

    for filename in os.listdir(image_dir):
        if filename.endswith('light.png'):
            # Paths for light and dark images
            light_image_file = os.path.join(image_dir, filename)
            dark_image_file = os.path.join(image_dir, filename.replace('light', 'dark'))
            output_image_path = os.path.join(output_dir, filename.replace('light.png', 'lightdark.png'))

            # Check if the dark image exists
            if not os.path.exists(dark_image_file):
                print(f"Dark mode image missing for: {filename}")
                continue

            # Load the images
            image1 = cv2.imread(light_image_file)
            image2 = cv2.imread(dark_image_file)

            if image1 is None or image2 is None:
                print(f"Error loading images: {light_image_file} or {dark_image_file}")
                continue

            # Concatenate images horizontally
            # side_by_side = np.hstack((image1, image2))

            # for dark to light conversion
            side_by_side = np.hstack((image2, image1))

            # Save the combined image
            cv2.imwrite(output_image_path, side_by_side)
            print(f"Saved combined image: {output_image_path}")

            ### Optionally display the combined image (comment out for batch processing)
            # cv2.imshow('Side by Side Images', side_by_side)
            # cv2.waitKey(0)  # Wait for a key press
            # cv2.destroyAllWindows()

            # results.append(output_image_path)  # Add to results list

    # return results  # Return list of saved image paths

# for dark to light
image_dir = '/path/to/automatic_inconsistency_detection/web_applications/shadow_reveal_truth/application_with_system_preferences/narcity/input/narcity'
output_dir = '/path/to/automatic_inconsistency_detection/web_applications/shadow_reveal_truth/application_with_system_preferences/narcity/input/side_by_side_visualization'

# Run the batch process
combine_image = get_image_side_by_side(image_dir, output_dir)
print("Batch Results:", combine_image)
