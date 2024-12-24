'''
Dawn being clarity - application only support dark mode and use extension to convert the application into light mode
check whether the text are complement blended with the background rendering the missing text

# new version -dec 9
'''


from typing import List, Dict, Any
from rapidfuzz import fuzz
import cv2
import json
import re
import numpy as np


def load_json(json_path: str) -> Dict[str, Any]:
    """Load JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    """Normalize text by converting to lowercase and removing extra spaces."""
    return re.sub(r'\s+', ' ', text.strip().lower())


def calculate_overlap(box1, box2):
    """Calculate the overlap area between two bounding boxes."""
    x1, y1, x2, y2 = max(box1[0], box2[0]), max(box1[1], box2[1]), min(box1[2], box2[2]), min(box1[3], box2[3])
    overlap_width = max(0, x2 - x1)
    overlap_height = max(0, y2 - y1)
    return overlap_width * overlap_height


def get_bounding_box_vertices(bbox):
    """Convert bounding box vertices into (x1, y1, x2, y2)."""
    x_coords = [v['x'] for v in bbox]
    y_coords = [v['y'] for v in bbox]
    return [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]


def is_similar(text1: str, text2: str, threshold: int = 85) -> bool:
    """Check similarity using fuzzy matching."""
    return fuzz.ratio(text1, text2) >= threshold


def extract_text_structure(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extracts the text and bounding box information for each word from the JSON data."""
    words_info = []
    for page in data["pages"]:
        for word in page["words"]:
            text_content = normalize_text(word['text'])
            bounding_box = get_bounding_box_vertices(word['boundingBox']['vertices'])
            words_info.append({
                "content": text_content,
                "bounding_box": bounding_box,
            })
    return words_info


def combine_nearby_boxes(text_elements: List[Dict[str, Any]], max_distance: int = 50) -> List[Dict[str, Any]]:
    """
    Combine nearby bounding boxes and their text content if they are close enough.
    """
    combined_texts = []
    used = set()

    for i, element1 in enumerate(text_elements):
        if i in used:
            continue
        current_box = element1['bounding_box']
        current_text = element1['content']
        for j, element2 in enumerate(text_elements):
            if i == j or j in used:
                continue
            other_box = element2['bounding_box']
            if abs(current_box[2] - other_box[0]) < max_distance or abs(current_box[0] - other_box[2]) < max_distance:
                if abs(current_box[1] - other_box[1]) < max_distance:
                    current_box = [
                        min(current_box[0], other_box[0]),
                        min(current_box[1], other_box[1]),
                        max(current_box[2], other_box[2]),
                        max(current_box[3], other_box[3]),
                    ]
                    current_text += element2['content']
                    used.add(j)
        combined_texts.append({
            "content": current_text,
            "bounding_box": current_box
        })
        used.add(i)

    return combined_texts


def find_missing_texts(light_texts: List[Dict[str, Any]], dark_texts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Find texts in light mode that are missing or mismatched in dark mode based on IoU and occurrences.

    Args:
        light_texts: List of text elements from the light mode.
        dark_texts: List of text elements from the dark mode.

    Returns:
        List of texts missing in the dark mode.
    """
    threshold = 75  # Fixed: was incorrectly defined as a tuple
    spatial_threshold = 0.5  # Fractional overlap threshold
    fuzz_threshold = 75

    missing_texts = []

    for dark_element in dark_texts:

        if len(dark_element['content'].strip()) <= 2 or dark_element['content'] in {',', '.', '!', '?', ' '}:
            continue
        text_found = False

        for light_element in light_texts:
            text_found = False
            # Check text similarity
            if is_similar(dark_element['content'], light_element['content'], threshold):
                # Check spatial overlap
                dark_bbox = dark_element['bounding_box']
                light_bbox = light_element['bounding_box']

                overlap_area = calculate_overlap(dark_bbox, light_bbox)
                light_area = (dark_bbox[2] - dark_bbox[0]) * (dark_bbox[3] - dark_bbox[1])
                if overlap_area / light_area > spatial_threshold:
                    text_found = True
                    break

            # recheck by combining the neighbour element

            if not text_found:
                combined_light_texts = combine_nearby_boxes(light_texts)
                for combined_light_element in combined_light_texts:
                    if is_similar(
                            dark_element['content'],
                            combined_light_element['content'],
                            fuzz_threshold

                    ):
                        dark_bbox = light_element['bounding_box']
                        light_bbox = combined_light_element['bounding_box']
                        overlap_area = calculate_overlap(dark_bbox, light_bbox)
                        dark_area = (dark_bbox[2] - dark_bbox[0]) * (dark_bbox[3] - dark_bbox[1])
                        if overlap_area / dark_area > spatial_threshold:
                            text_found = True
                            break

        if not text_found:
            missing_texts.append(dark_element)

    return missing_texts


def save_missing_info_to_json(missing_elements: List[Dict[str, Any]], output_json_path: str):
    """Save missing information to a JSON file."""
    with open(output_json_path, 'w') as file:
        json.dump(missing_elements, file, indent=4)


def missing_text(light_image_path: str, dark_image_path: str, light_json_path: str, dark_json_path: str,
                 output_image_path: str, output_json_path: str):
    """Visualize the side-by-side comparison and highlight missing areas."""
    light_img = cv2.imread(light_image_path)
    dark_img = cv2.imread(dark_image_path)
    summary_data = []

    if light_img is None or dark_img is None:
        print("Error: Could not load images.")
        return

    if light_img.shape[:2] != dark_img.shape[:2]:
        dark_img = cv2.resize(dark_img, (light_img.shape[1], light_img.shape[0]))

    light_json = load_json(light_json_path)
    dark_json = load_json(dark_json_path)

    light_texts = extract_text_structure(light_json)
    dark_texts = extract_text_structure(dark_json)

    missing_texts = find_missing_texts(light_texts, dark_texts)

    for elem in missing_texts:
        bbox = elem['bounding_box']
        cv2.rectangle(light_img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)

    combined_image = np.hstack((dark_img, light_img))

    cv2.imwrite(output_image_path, combined_image)
    save_missing_info_to_json(missing_texts, output_json_path)

    summary_data = {
        "file": output_json_path,
        "missing_texts": len(missing_texts)
    }

    # print(f"Output saved at: {output_image_path}")
    # print(f"Missing information saved at: {output_json_path}")

    return summary_data