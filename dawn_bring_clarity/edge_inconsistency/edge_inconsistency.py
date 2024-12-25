
'''
The process identify the edge inconsistency to the pair of screenshot where the application only support the dark mode
and use extension to convert into the light mode
'''


import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.spatial import cKDTree  # Efficient for nearest-neighbor search


# Directory containing light and dark mode images
input_dir = 'path/to/automatic_inconsistency_detection/web_applications/dawn_bring_clarity/application_with_only_dark_mode/courseforge/input/courseforge'
output_dir = 'path/to/automatic_inconsistency_detection/web_applications/dawn_bring_clarity/application_with_only_dark_mode/courseforge/output/edge_inconsistency'


# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define the distance threshold
DISTANCE_THRESHOLD = 3  # Adjust this value for sensitivity (in pixels)

# Process each pair of light and dark images
dark_images = [f for f in os.listdir(input_dir) if f.endswith('dark.png')]
light_images = [f.replace('dark', 'light') for f in dark_images]

for dark_image_name, light_image_name in zip(dark_images, light_images):
    dark_image_path = os.path.join(input_dir, dark_image_name)
    light_image_path = os.path.join(input_dir, light_image_name)

    # Load the images
    dark_image = cv2.imread(dark_image_path)
    light_image = cv2.imread(light_image_path)


    if dark_images is None or light_image is None:
        print(f"Error: Could not load images {dark_image_path} or {light_image_path}")
        continue

    if dark_image.shape != light_image.shape:
        print(f"Error: Size mismatch {dark_image_path} and {light_image_path}")
        continue

    # Convert to grayscale
    dark_gray = cv2.cvtColor(dark_image, cv2.COLOR_BGR2GRAY)
    light_gray = cv2.cvtColor(light_image, cv2.COLOR_BGR2GRAY)


    # Apply Gaussian blurring to reduce noise
    dark_gray_blurred = cv2.GaussianBlur(dark_gray, (5, 5), 0)
    light_gray_blurred = cv2.GaussianBlur(light_gray, (5, 5), 0)

    # Apply Canny edge detection with adjusted threshold
    dark_edges = cv2.Canny(dark_gray, 10, 55)
    light_edges = cv2.Canny(light_gray, 10, 55)

    # Extract edge coordinates (non-zero pixels)
    dark_coords = np.column_stack(np.where(dark_edges > 0))
    light_coords = np.column_stack(np.where(light_edges > 0))


    # Create KD-trees for efficient nearest-neighbor search
    dark_tree = cKDTree(dark_coords)
    light_tree = cKDTree(light_coords)

    # Find problematic edges in dark mode
    distances_dark, _ = light_tree.query(dark_coords)
    problematic_dark_coords = dark_coords[distances_dark > DISTANCE_THRESHOLD]

    # Find problematic edges in light mode
    distances_light, _ = dark_tree.query(light_coords)
    problematic_light_coords = light_coords[distances_light > DISTANCE_THRESHOLD]

    # Create blank masks for visualization
    problematic_dark = np.zeros_like(dark_edges, dtype=np.uint8)
    problematic_light = np.zeros_like(light_edges, dtype=np.uint8)


    # Mark problematic edges
    problematic_dark[problematic_dark_coords[:, 0], problematic_dark_coords[:, 1]] = 255
    problematic_light[problematic_light_coords[:, 0], problematic_light_coords[:, 1]] = 255

    # Combine problematic edges for visualization
    combined_problematic = cv2.bitwise_or(problematic_dark, problematic_light)

    # Create a color overlay for problematic areas
    highlight_overlay = np.zeros_like(dark_image, dtype=np.uint8)
    highlight_overlay[problematic_dark > 0] = [0, 0, 255]  # Red for dark-only edges
    highlight_overlay[problematic_light > 0] = [0, 255, 0]  # Green for light-only edges

    # Overlay the highlights on the original light mode image
    highlighted_light = cv2.addWeighted(light_image, 0.7, highlight_overlay, 1, 0)

    # Create Color Overlay
    color_overlay = np.zeros((light_edges.shape[0], light_edges.shape[1], 3), dtype=np.uint8)

    color_overlay[:, :, 2] = dark_edges
    color_overlay[:, :, 1] = light_edges

    # Save results
    base_name = dark_image_name.replace('dark.png', '')
    cv2.imwrite(os.path.join(output_dir, f'{base_name}_highlighted_light.png'), highlighted_light)
    cv2.imwrite(os.path.join(output_dir, f'{base_name}_problematic_areas.png'), combined_problematic)
    cv2.imwrite(os.path.join(output_dir, f'{base_name}_overlay_inconsistency.png'), color_overlay)


    # Display results for quick inspection
    plt.figure(figsize=(15, 10))
    plt.subplot(1, 3, 1)
    plt.title("Light Mode Edges")
    plt.imshow(light_edges, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title("Dark Mode Edges")
    plt.imshow(dark_edges, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title("Highlighted Problematic Areas")
    plt.imshow(cv2.cvtColor(highlighted_light, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.tight_layout()
    # plt.show()

print("Edge detection processing complete.")