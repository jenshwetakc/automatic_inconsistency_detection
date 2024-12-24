import requests
import json
import cv2
import numpy as np
import os

# Set your Upstage API key
api_key = ""

# Path to the single image
image_path = "/path/to/your/single_image.png"

# Output folder for results
output_folder = "/path/to/output/folder"

# Make sure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Upstage OCR API endpoint
url = "https://api.upstage.ai/v1/document-ai/ocr"
headers = {"Authorization": f"Bearer {api_key}"}

# Extract the base filename (without extension)
base_filename = os.path.splitext(os.path.basename(image_path))[0]

# Send the image to the OCR API
with open(image_path, "rb") as image_file:
    files = {"document": image_file}
    response = requests.post(url, headers=headers, files=files)

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON response
        ocr_result = response.json()

        # Save the OCR result to a JSON file
        json_output_path = os.path.join(output_folder, f"{base_filename}.json")
        with open(json_output_path, "w") as json_file:
            json.dump(ocr_result, json_file, indent=4)

        print(f"OCR results for {base_filename} saved to {json_output_path}")

        # Load the original image
        image = cv2.imread(image_path)

        # Loop through each page and word to get bounding box information
        for page in ocr_result['pages']:
            for word in page['words']:
                # Get the vertices of the bounding box
                vertices = word['boundingBox']['vertices']

                # Extract the coordinates (x, y) from each vertex
                pts = [(v['x'], v['y']) for v in vertices]

                # Convert list of points to NumPy array
                pts = np.array(pts, np.int32)
                pts = pts.reshape((-1, 1, 2))

                # Draw the bounding box (polygon) on the image
                cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Save the image with bounding boxes
        output_image_path = os.path.join(output_folder, f"{base_filename}_with_boxes.png")
        cv2.imwrite(output_image_path, image)

        print(f"Image with bounding boxes saved as {output_image_path}")
    else:
        print(f"Error processing {base_filename}: {response.status_code} - {response.text}")
