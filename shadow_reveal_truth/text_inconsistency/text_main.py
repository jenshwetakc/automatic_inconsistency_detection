# *******
# october 25

'''
Shadow reveal truth - application that support light and dark mode
- application support light and dark mode with toggle button
- application based on system preference
- application, used extension to convert into the dark mode
'''

import json
import os

from shadow_reveal_truth.text_inconsistency.invisible_text import invisible_text_inconsistency
from shadow_reveal_truth.text_inconsistency.missing_text import missing_text


def merge_json_results(output_json_1: str, output_json_2: str, merged_output_path: str):
    """Merge the results of two JSON files into one."""
    with open(output_json_1, 'r') as f1, open(output_json_2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Merge the data from both JSON files
    merged_data = {
        "contrast_check": data1,
        "missing_texts": data2
    }

    # Save the merged data into a new JSON file
    os.makedirs(os.path.dirname(merged_output_path), exist_ok=True)
    with open(merged_output_path, 'w') as f_out:
        json.dump(merged_data, f_out, indent=4)

    print(f"Merged output saved to {merged_output_path}")


def process_batch(image_dir, json_dir, output_dir):
    """Process a batch of images and JSON files for invisible and missing text checks, with separate summaries."""
    # Define reusable directories
    missing_text_dir = os.path.join(output_dir, 'missing_text')
    invisible_text_dir = os.path.join(output_dir, 'invisible_text')
    merge_dir = os.path.join(output_dir, 'merged_output')


    # Ensure output directories exist
    os.makedirs(missing_text_dir, exist_ok=True)
    os.makedirs(invisible_text_dir, exist_ok=True)

    # Initialize separate summaries for each type
    missing_text_summary = []
    invisible_text_summary = []

    # Sort files in ascending order
    files = sorted(
        [f for f in os.listdir(image_dir) if f.endswith('light.png')],
        key=lambda x: int(x.split('light')[0]) if x.split('light')[0].isdigit() else x
    )

    for filename in files:
        try:
            # Define base filename
            base_filename = filename.replace('light.png', '')

            # Input files
            light_image_file = os.path.join(image_dir, filename)
            dark_image_file = os.path.join(image_dir, filename.replace('light', 'dark'))

            # JSON paths
            light_json_file = os.path.join(json_dir, f"{base_filename}light.json")
            dark_json_file = os.path.join(json_dir, f"{base_filename}dark.json")

            # Output files for missing and invisible text
            missing_text_output = os.path.join(missing_text_dir, f"{base_filename}missing.png")
            missing_text_json = os.path.join(missing_text_dir, f"{base_filename}missing.json")

            invisible_text_output = os.path.join(invisible_text_dir, f"{base_filename}invisible.png")
            invisible_text_json = os.path.join(invisible_text_dir, f"{base_filename}invisible.json")

            merged_output_dir = os.path.join(merge_dir, f"{base_filename}merged_output.json")


            ## Process invisible text inconsistencies
            invisible_summary = invisible_text_inconsistency(
                light_image_file, dark_image_file, light_json_file, dark_json_file,
                invisible_text_output, invisible_text_json
            )

           ## Process missing text inconsistencies
            missing_summary = missing_text(
                light_image_file, dark_image_file, light_json_file, dark_json_file,
                missing_text_output, missing_text_json
            )

            merge_json_results(invisible_text_json, missing_text_json, merged_output_dir)


            ## Add to respective summaries
            invisible_text_summary.append({
                "file": base_filename,
                "invisible_text_summary": invisible_summary
            })

            missing_text_summary.append({
                "file": base_filename,
                "missing_text_summary": missing_summary
            })

        except Exception as e:
            print(f"Error processing file {base_filename}: {e}")
            missing_text_summary.append({
                "file": base_filename,
                "error": str(e)
            })
            invisible_text_summary.append({
                "file": base_filename,
                "error": str(e)
            })

    # Sort summaries in ascending order by file name
    missing_text_summary.sort(key=lambda x: x['file'])
    invisible_text_summary.sort(key=lambda x: x['file'])

    # Save separate summary files in corresponding directories
    missing_summary_path = os.path.join(missing_text_dir, 'summary.json')
    invisible_summary_path = os.path.join(invisible_text_dir, 'summary.json')

    with open(missing_summary_path, 'w') as missing_file:
        json.dump(missing_text_summary, missing_file, indent=4)

    with open(invisible_summary_path, 'w') as invisible_file:
        json.dump(invisible_text_summary, invisible_file, indent=4)

    print(f"Batch processing completed. Missing text summary saved to {missing_summary_path}.")
    print(f"Batch processing completed. Invisible text summary saved to {invisible_summary_path}.")



def main():
   # upstage ocr
    image_dir = 'path to image directory (original  light and dark mode screenshot)'
    json_dir = 'path to json file from ocr'
    output_dir = 'output directory'
    # Process the batch of images
    process_batch(image_dir, json_dir, output_dir)

if __name__ == '__main__':
    main()