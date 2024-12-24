'''
Shadow reveal truth - application that support light and dark mode
- application support light and dark mode with toggle button
- application based on system preference
- application, used extension to convert into the dark mode
identify the missing text inconsistency for single image

'''

import json
import cv2

def preprocess_text(text):
    """Normalize text to overcome common issues like case sensitivity, punctuation, and spacing."""
    import string
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())

def draw_bounding_boxes_for_missing_text(light_json_path, dark_json_path, light_image_path, output_image_path):
    """Draw bounding boxes for missing text on the light image."""

    # Load the light and dark JSON files
    with open(light_json_path, 'r', encoding='utf-8') as light_file:
        light_json = json.load(light_file)
    with open(dark_json_path, 'r', encoding='utf-8') as dark_file:
        dark_json = json.load(dark_file)

    # Extract text with preprocessing
    light_texts = {preprocess_text(word['text']): word for page in light_json['pages'] for word in page['words']}
    dark_texts = {preprocess_text(word['text']) for page in dark_json['pages'] for word in page['words']}

    # Identify missing texts
    missing_texts = set(light_texts.keys()) - dark_texts

    # Load the light mode image
    image = cv2.imread(light_image_path)

    # Draw bounding boxes for missing texts
    for text in missing_texts:
        word = light_texts[text]
        vertices = word['boundingBox']['vertices']
        x1, y1 = vertices[0]['x'], vertices[0]['y']
        x2, y2 = vertices[2]['x'], vertices[2]['y']

        # Draw the bounding box on the image
        cv2.rectangle(image, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
        # Optionally, put the text label
        cv2.putText(image, word['text'], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Save the output image
    cv2.imwrite(output_image_path, image)
    print(f"Output image with bounding boxes saved to: {output_image_path}")


light_image_path = 'Path to the light mode image'
dark_image_path = 'Path to the dark mode image'
light_json_path = 'Path to the light mode OCR output JSON file'
dark_json_path = 'Path to the dark mode OCR output JSON file'
output_image_path = 'Path to save the output image'
output_json_path = 'Path to save the output JSON file'

# Run the function
draw_bounding_boxes_for_missing_text(light_json_path, dark_json_path, light_image_path, output_image_path)
