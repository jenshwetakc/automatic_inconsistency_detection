
###
'''
Dawn being clarity - application only support dark mode and use extension to convert the application into light mode


'''
import os

import cv2
import math
import numpy as np
import json
from typing import List, Dict, Any
from collections import Counter

# Load the JSON file
def load_json(json_path: str) -> Dict[str, Any]:
    """Load JSON file."""
    # code update, november 18
    # Ticket: I-TI3,
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found at path: {json_path}")
    with open(json_path, 'r') as f:
        return json.load(f)

# Function to save information to JSON
def save_failed_contrast_info_to_json(failed_texts: List[Dict[str, Any]], output_json_path: str):
    """Save text elements that fail the contrast ratio check to a JSON file."""
    with open(output_json_path, 'w') as file:
        json.dump(failed_texts, file, indent=4)

# Extract bounding box  from vertices
def extract_bounding_box(text_info):
    """Extract bounding box coordinates from the text information."""
    vertices = text_info['boundingBox']['vertices']
    xmin = min([v['x'] for v in vertices])
    ymin = min([v['y'] for v in vertices])
    xmax = max([v['x'] for v in vertices])
    ymax = max([v['y'] for v in vertices])
    return xmin, ymin, xmax, ymax


def bgr_to_rgb(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb



# issues:
# november 18
# ticket: I-TI-4
def get_color_pixel_value(image, text_info):
    # Get bounding box
    x_min, y_min, x_max, y_max = extract_bounding_box(text_info)

    # Clamp coordinates within image bounds
    height, width = image.shape[:2]
    x_min, y_min = max(0, x_min), max(0, y_min)
    x_max, y_max = min(width, x_max), min(height, y_max)

    points = np.array([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]])

    color_pixel_values = []
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            if cv2.pointPolygonTest(points, (x, y), False) >= 0:
                color_pixel_values.append(tuple(image[y, x]))

    # Count the occurrence of each unique color
    color_counts = Counter(color_pixel_values)
    # Get the most common colors
    most_common_colors = color_counts.most_common(min(len(color_counts), 200))

    return most_common_colors


def calculate_std_deviation(image, text_info):

    image_rgb = bgr_to_rgb(image)
    # Get bounding box coordinates
    x_min, y_min, x_max, y_max = extract_bounding_box(text_info)

    # Define the bounding box points as a quadrilateral
    points = np.array([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]], dtype=np.int32)

    # create a mask for the bounding box region
    mask = np.zeros(image_rgb.shape[:2], dtype=np.uint8)
    polygon = np.array(points, dtype=np.int32)
    # cv2.fillPoly(mask, [polygon], 255)
    cv2.fillPoly(mask, [points.reshape((-1, 1, 2))], 255)

    roi = cv2.bitwise_and(image_rgb, image, mask=mask)
    roi_pixels = roi[mask == 255].reshape(-1 ,3)

    all_pixels_array = np.array(roi_pixels)

    std_dev = np.std(all_pixels_array)
    return std_dev

def is_large_text(text_info) -> bool:
    """Check if the text is large based on the height of the bounding box."""
    x_min, y_min, x_max, y_max = extract_bounding_box(text_info)
    text_height = y_max -y_min
    # print(text_info)
    # print(text_height)
    large_text_threshold = 24  # Threshold for large text (e.g., 18-point or larger)
    return text_height >= large_text_threshold


def get_contrast_ratio(foreground_color, background_color):
    """Calculate contrast ratio between text and background."""

    def relative_luminance(color):
        color = np.array(color) / 255.0
        R, G, B = color
        R = R / 12.92 if R <= 0.04045 else ((R + 0.055) / 1.055) ** 2.4
        G = G / 12.92 if G <= 0.04045 else ((G + 0.055) / 1.055) ** 2.4
        B = B / 12.92 if B <= 0.04045 else ((B + 0.055) / 1.055) ** 2.4
        return 0.2126 * R + 0.7152 * G + 0.0722 * B

    L1 = relative_luminance(foreground_color)
    L2 = relative_luminance(background_color)
    # def luminance(color):
    #     """Calculate the luminance of a color in RGB format."""
    #     rgb = [channel / 255.0 for channel in color]
    #     rgb = [((c + 0.055) / 1.055) ** 2.4 if c > 0.03928 else c / 12.92 for c in rgb]
    #     return 0.2126 * rgb[2] + 0.7152 * rgb[1] + 0.0722 * rgb[0]

    # L1 = luminance(foreground_color)
    # L2 = luminance(background_color)

    if L1 > L2:
        return (L1 + 0.05) / (L2 + 0.05)
    else:
        return (L2 + 0.05) / (L1 + 0.05)


# Convert RGB to HSV and identify color family
def rgb_to_hsv(rgb_color):
    """Convert RGB to HSV color space."""
    rgb_normalized = np.array(rgb_color) / 255.0
    hsv_color = cv2.cvtColor(np.uint8([[rgb_normalized * 255]]), cv2.COLOR_RGB2HSV)[0][0]
    return hsv_color


def rgb_to_hsl(rgb_color):
    """Convert RGB to HSL color space."""
    rgb_normalized = np.array(rgb_color) / 255.0
    hsl_color = cv2.cvtColor(np.uint8([[rgb_normalized * 255]]), cv2.COLOR_RGB2HLS)[0][0]
    return hsl_color


def is_light_or_dark(hsl_color):
    """Determine if the color is light or dark based on the lightness value in HSL."""
    lightness = hsl_color[1] / 255.0  # Normalize the lightness value to be between 0 and 1
    if lightness >= 0.8:
        return "light"
    elif lightness <= 0.2:
        return "dark"
    else:
        return "neutral"


def analyze_text_background_colors_hsl(text_color, background_color):
    """Determine if the text and background fall under problematic categories using HSL."""
    hsl_text = rgb_to_hsl(text_color)
    hsl_background = rgb_to_hsl(background_color)

    txt_brightness = is_light_or_dark(hsl_text)
    bg_brightness = is_light_or_dark(hsl_background)

    if txt_brightness == "light" and bg_brightness == "light":
        return "Light text on light background"
    elif txt_brightness == "dark" and bg_brightness == "dark":
        return "Dark text on dark background"
    # else:
    #     return "Color contrast issue"

    # Check for color saturation issues (e.g., muted colors)
    text_saturation = hsl_text[1]
    background_saturation = hsl_background[1]
    # print('saturation',text_saturation)
    # print('background color',background_saturation)
    if text_saturation < 50 and background_saturation < 50:
        return "Low saturation - muted colors"

    # Default case for general contrast issue
    return "Color contrast issue"


def euclidean_distance(color1, color2):
    """Calculate the Euclidean distance between two colors in BGR format."""
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


def convert_color_format(bgr_color):
    # color_rgb = (int(bgr_color[2]), int(bgr_color[1]), int(bgr_color[0]))
    color_rgb = (float(bgr_color[2]), float(bgr_color[1]), float(bgr_color[0]))
    return color_rgb


def check_contrast_and_draw_bounding_boxes(light_image, dark_image, light_texts, dark_texts, output_image_path,
                                           output_json_path):
    """Check the contrast ratio for both light and dark mode images, draw bounding boxes, and save failing cases."""
    minimum_contrast_ratio_normal = 4.5  # WCAG minimum contrast ratio for regular text
    minimum_contrast_ratio_large = 3.0  # WCAG minimum contrast ratio for large text

    test_threshold = 2.5
    failed_texts = []  # List to store texts that fail the contrast check
    std_threshold = 20  # Standard deviation threshold

    # Dictionary to store text that passes the contrast in light mode
    dark_mode_pass = {}

    # Light mode contrast check
    print('dark mode')
    for page in dark_texts['pages']:
        for text in page['words']:
            # print(is_large_text(text))

            contrast_threshold = minimum_contrast_ratio_large if is_large_text(text) else minimum_contrast_ratio_normal
            std = calculate_std_deviation(dark_image, text)

            # Ticket: I-TI1 start
            # text_color_bgr, background_color_bgr, remaining_colors = get_color_pixel_value(light_image, text)
            most_common_colors = get_color_pixel_value(dark_image, text)

            if len(most_common_colors) >= 2:
                background_color_bgr = most_common_colors[0][0]
                text_color_bgr = most_common_colors[1][0]

            remaining_colors = most_common_colors[2:]

            # Ticket: I-TI1 end

            background_color = convert_color_format(background_color_bgr)
            text_color = convert_color_format(text_color_bgr)
            contrast = get_contrast_ratio(text_color, background_color)
            # print(f"Text: {text['text']}")
            # print('Text color:', text_color)
            # print('backgound color', background_color)
            # print('contrast', contrast)
            #
            # print('remaining color', remaining_colors)
            # print('Text color:', text_color_bgr)

            # If contrast fails in light mode
            if contrast < contrast_threshold:

                # print(f"Text: {text['text']}")
                # print('Text color:', text_color)
                # print('backgound color', background_color)
                # print('contrast', contrast)
                #
                # print('remaining color', remaining_colors)
                # print('Text color:', text_color_bgr)

                # Attempt to adjust text color if needed
                text_color_candidates = [color[0] for color in remaining_colors]
                if text_color_candidates:
                    #  ticket: I- TI-5
                    background_color_bgr = np.array(background_color_bgr, dtype=np.int32)
                    text_color_candidates = [np.array(color, dtype=np.int32) for color in text_color_candidates]

                    new_text_color_bgr = max(text_color_candidates,
                                             key=lambda color: euclidean_distance(background_color_bgr, color))
                    new_text_color = convert_color_format(new_text_color_bgr)
                    new_ratio = get_contrast_ratio(new_text_color, background_color)
                    print("new text color", new_text_color)

                    # If the new contrast ratio still fails
                    if new_ratio < contrast_threshold:


                        # if new_ratio < test_threshold and contrast < test_threshold:
                        if new_ratio < test_threshold:
                            failed_texts.append({
                                "Mode": "Dark",
                                "Text": text['text'],
                                "Text color one": text_color,
                                "contrast one": contrast,
                                "Text Color": new_text_color,
                                "Background Color": background_color,
                                'contrast threshold': contrast_threshold,
                                "Contrast Ratio": new_ratio,
                                "Failure Category": failure_category,
                                "Bounding Box": extract_bounding_box(text)
                            })
                            # Draw bounding box on light image
                            # x_min, y_min, x_max, y_max = extract_bounding_box(text)
                            # cv2.rectangle(light_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

                        # if new_ratio < test_threshold:
                        #     x_min, y_min, x_max, y_max = extract_bounding_box(text)
                        #     cv2.rectangle(dark_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

                    else:
                        # Save as passed with adjusted color
                        dark_mode_pass[text['text']] = {
                            "Bounding Box": extract_bounding_box(text),
                            "Text Color": new_text_color,
                            "Background Color": background_color,
                            "Contrast Ratio": new_ratio
                        }
            else:
                # If contrast passes in light mode, save the info for later comparison with dark mode
                dark_mode_pass[text['text']] = {
                    "Bounding Box": extract_bounding_box(text),
                    "Text Color": text_color,
                    "Background Color": background_color,
                    "Contrast Ratio": contrast
                }

    # Dark mode contrast check
    print('light mode')
    for page in light_texts['pages']:
        for text in page['words']:
            contrast_threshold = minimum_contrast_ratio_large if is_large_text(text) else minimum_contrast_ratio_normal
            std = calculate_std_deviation(light_image, text)
            # text_color_bgr, background_color_bgr, remaining_colors_bgr = get_color_pixel_value(dark_image, text)

            most_common_colors = get_color_pixel_value(light_image, text)

            if len(most_common_colors) >= 2:
                background_color_bgr = most_common_colors[0][0]
                text_color_bgr = most_common_colors[1][0]
                # print(text_color)
            # else:
            #     print('no color found') # update this one later

            remaining_colors_bgr = most_common_colors[2:]

            background_color = convert_color_format(background_color_bgr)
            text_color = convert_color_format(text_color_bgr)
            contrast = get_contrast_ratio(text_color, background_color)
            text_content = text['text']

            # If contrast fails in dark mode
            if contrast < contrast_threshold:
                # Attempt to adjust text color if needed
                text_color_candidates = [color[0] for color in remaining_colors_bgr]
                if text_color_candidates:
                    #  ticket: I- TI-5
                    background_color_bgr = np.array(background_color_bgr, dtype=np.int32)
                    text_color_candidates = [np.array(color, dtype=np.int32) for color in text_color_candidates]

                    new_text_color_bgr = max(text_color_candidates,
                                             key=lambda color: euclidean_distance(background_color_bgr, color))
                    new_text_color = convert_color_format(new_text_color_bgr)
                    new_ratio = get_contrast_ratio(new_text_color, background_color)

                    # If the new contrast ratio still fails
                    if new_ratio < contrast_threshold:
                        failure_category = analyze_text_background_colors_hsl(new_text_color, background_color)
                        if text_content in dark_mode_pass:
                            # If the text passed contrast in light mode but failed in dark mode, label as "text inconsistency"
                            light_contrast = dark_mode_pass[text_content]["Contrast Ratio"]
                            print(light_contrast)

                            if light_contrast >= contrast_threshold:
                                # if light_contrast > new_ratio:
                                failure_reason = "text inconsistency"
                            else:
                                failure_reason = "contrast ratio issue"
                        else:
                            # If the text also fails in light mode, label as "contrast ratio issue"
                            failure_reason = "contrast ratio issue"

                        # Append failure information

                        # failed_texts.append({
                        #     "Mode": "dark",
                        #     "Text": text_content,
                        #     "Text Color": new_text_color,
                        #     "Background Color": background_color,
                        #     "Contrast Ratio": new_ratio,
                        #     "Failure Reason": failure_reason,
                        #     "Failure Category": failure_category,
                        #     "Bounding Box": extract_bounding_box(text)
                        # })

                        # x_min, y_min, x_max, y_max = extract_bounding_box(text)
                        # cv2.rectangle(dark_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

                        # update november18
                        # test contrast
                        # if new_ratio < test_threshold and contrast < test_threshold:
                        if new_ratio < test_threshold:
                            failed_texts.append({
                                "Mode": "Light",
                                "Text": text_content,
                                "Text color one": text_color,
                                "contrast one": contrast,
                                "Text Color": new_text_color,
                                "Background Color": background_color,
                                "Contrast Ratio": new_ratio,
                                "Failure Reason": failure_reason,
                                "Failure Category": failure_category,
                                "Bounding Box": extract_bounding_box(text)
                            })
                            x_min, y_min, x_max, y_max = extract_bounding_box(text)
                            cv2.rectangle(light_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

                        # October 31
                        # update the code logic, and draw the bounding box if the issues is inconsistency issues
                        # if failure_reason == "text inconsistency":
                        #     x_min, y_min, x_max, y_max = extract_bounding_box(text)
                        #     cv2.rectangle(dark_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

    # Save all failed contrast information to JSON
    save_failed_contrast_info_to_json(failed_texts, output_json_path)

    # place the dark image on left and light image on right
    # Combine images for visualization and save
    combined_image = np.hstack((dark_image, light_image))
    cv2.imwrite(output_image_path, combined_image)

    # save only if there is contrast issues
    # if failed_texts:
    #     save_failed_contrast_info_to_json(failed_texts, output_json_path)
    #
    #     # Combine images for visualization and save
    #     combined_image = np.hstack((light_image, dark_image))
    #     cv2.imwrite(output_image_path, combined_image)


# code update
# november 19
# Ticket: I-TI3

def load_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Failed to load image at path: {image_path}")
    return image


def invisible_text_inconsistency(light_image_path: str, dark_image_path: str, light_json_path: str, dark_json_path: str,
                                 output_image_path: str, output_json_path: str):
    """Check contrast for both light and dark mode, draw bounding boxes, and save failing cases."""
    # Load images
    # light_img = cv2.imread(light_image_path)
    # dark_img = cv2.imread(dark_image_path)
    # code update
    # november 19
    # Ticket: I-TI3

    light_img = load_image(light_image_path)
    dark_img = load_image(dark_image_path)

    light_rgb = bgr_to_rgb(light_img)
    dark_rgb = bgr_to_rgb(dark_img)

    if light_img is None or dark_img is None:
        print(f"Error: Image not found or cannot be read at specified paths.")
        return

    # Ticket- dark to light
    if dark_img.shape[:2] != light_img.shape[:2]:
        # Resize dark image to match the light image dimensions
        light_img = cv2.resize(light_img, (dark_img.shape[1], dark_img.shape[0]))

    # Load JSON data
    light_json_data = load_json(light_json_path)
    dark_json_data = load_json(dark_json_path)

    check_contrast_and_draw_bounding_boxes(light_img, dark_img, light_json_data, dark_json_data, output_image_path,
                                           output_json_path)


if __name__ == '__main__':

    light_image_path = 'Path to the light mode image'
    dark_image_path = 'Path to the dark mode image'
    light_json_path = 'Path to the light mode OCR output JSON file'
    dark_json_path = 'Path to the dark mode OCR output JSON file'
    output_image_path = 'Path to save the output image'
    output_json_path = 'Path to save the output JSON file'

    print(output_json_path)

    invisible_text_inconsistency(light_image_path, dark_image_path, light_json_path, dark_json_path, output_image_path, output_json_path)