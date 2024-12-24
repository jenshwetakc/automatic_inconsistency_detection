
###


'''
Shadow reveal truth - application that support light and dark mode
- application support light and dark mode with toggle button
- application based on system preference
- application, used extension to convert into the dark mode
'''





import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.metrics import structural_similarity as ssim
from scipy.spatial import cKDTree  # Efficient for nearest-neighbor search


# Directory containing light and dark mode images
light_image_path = '/path/to/light mode screenshot'
dark_image_path = '/path/to/dark mode screenshot'
output_dir = '/path/to/output/folder'


DISTANCE_THRESHOLD = 3

# Load the images
light_image = cv2.imread(light_image_path)
dark_image = cv2.imread(dark_image_path)

if light_image is None or dark_image is None:
    print(f"Error: Could not load images {light_image_path} or {dark_image_path}")
    exit()

if light_image.shape != dark_image.shape:
    print(f"Error: Size mismatch {light_image_path} and {dark_image_path}")
    exit()

# Convert to grayscale
light_gray = cv2.cvtColor(light_image, cv2.COLOR_BGR2GRAY)
dark_gray = cv2.cvtColor(dark_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blurring to reduce noise
light_gray_blurred = cv2.GaussianBlur(light_gray, (5, 5), 0)
dark_gray_blurred = cv2.GaussianBlur(dark_gray, (5, 5), 0)



# Apply Canny edge detection with adjusted threshold
light_edges = cv2.Canny(light_gray, 10, 55)
dark_edges = cv2.Canny(dark_gray, 10, 55)


# Extract edge coordinates (non-zero pixels)
light_coords = np.column_stack(np.where(light_edges > 0))
dark_coords = np.column_stack(np.where(dark_edges > 0))

# Create KD-trees for efficient nearest-neighbor search
light_tree = cKDTree(light_coords)
dark_tree = cKDTree(dark_coords)

# Find problematic edges in light mode
distances_light, _ = dark_tree.query(light_coords)
problematic_light_coords = light_coords[distances_light > DISTANCE_THRESHOLD]

# Find problematic edges in dark mode
distances_dark, _ = light_tree.query(dark_coords)
problematic_dark_coords = dark_coords[distances_dark > DISTANCE_THRESHOLD]

# Create blank masks for visualization
problematic_light = np.zeros_like(light_edges, dtype=np.uint8)
problematic_dark = np.zeros_like(dark_edges, dtype=np.uint8)

# Mark problematic edges
problematic_light[problematic_light_coords[:, 0], problematic_light_coords[:, 1]] = 255
problematic_dark[problematic_dark_coords[:, 0], problematic_dark_coords[:, 1]] = 255

# Combine problematic edges for visualization
combined_problematic = cv2.bitwise_or(problematic_light, problematic_dark)

# Create a color overlay for problematic areas
highlight_overlay = np.zeros_like(light_image, dtype=np.uint8)
highlight_overlay[problematic_light > 0] = [0, 0, 255]  # Red for light-only edges
highlight_overlay[problematic_dark > 0] = [0, 255, 0]  # Green for dark-only edges

# Overlay the highlights on the original light mode image
highlighted_light = cv2.addWeighted(dark_image, 0.7, highlight_overlay, 1, 0)

# Create Color Overlay

color_overlay = np.zeros((light_edges.shape[0], light_edges.shape[1], 3), dtype=np.uint8)

color_overlay[:, :, 2] = light_edges
color_overlay[:, :, 1] = dark_edges


cv2.imwrite(os.path.join(output_dir, f'{output_dir}_highlighted_light.png'), highlighted_light)
cv2.imwrite(os.path.join(output_dir, f'{output_dir}_problematic_areas.png'), combined_problematic)
cv2.imwrite(os.path.join(output_dir, f'{output_dir}_overlay_inconsistency.png'), color_overlay)


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

print("single image processing complete.")
