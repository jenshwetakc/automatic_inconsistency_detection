## Requirement 
- python 

Repository architecture
![](/Users/shwetakc/Desktop/Screenshot 2024-12-25 at 6.24.30 PM.png)


# Process to replicate the inconsistency detection 
1. Start from scratch 
   - Collect the dataset 
   - Select the pair of screenshot 
   - Run the detection 
     - To check the inconsistency from light to dark mode conversion use directory shadow_reveal_truth
     - To check the inconsistency for those application that only support dark mode and use extension to convert into light mode use directory dawn_bring_clarity 
     
2. Quick run
   - Select any application from the dataset 
   - Edge detection: Run (path/to/automated_darklight_inconsistency_detection/shadow_reveal_truth/edge_inconsistency/edge_inconsistency.py)
   
     - input directory: (path/to/automated_darklight_inconsistency_detection/web_application/app_with_extension/dark_mode_for_web/buzzfeed/input/buzzfeed)
     - output_directory: (path/to/automated_darklight_inconsistency_detection/web_application/app_with_extension/dark_mode_for_web/buzzfeed/output/edge_inconsistency)
     
   - Text_detection: (/automated_darklight_inconsistency_detection/shadow_reveal_truth/text_inconsistency/batch/text_main.py)
     - input_directory:  (path/to/automated_darklight_inconsistency_detection/web_application/app_with_extension/dark_mode_for_web/buzzfeed/input/buzzfeed)
     - json_directory:  (path/to/automated_darklight_inconsistency_detection/web_application/app_with_extension/dark_mode_for_web/buzzfeed/input/ocr)
     - output_directory: path/to/automated_darklight_inconsistency_detection/web_application/app_with_extension/dark_mode_for_web/buzzfeed/output/text_inconsistency



## Collect the Dataset

1. Collect Screenshots:

   Capture screenshots of the web application in both light and dark modes.
    
2. Pair the Screenshots:
   
    Match each light mode screenshot with its corresponding dark mode screenshot.
   
3. Rename the Screenshots:
   
    Use the naming convention: 1light.png for light mode and 1dark.png for dark mode, ensuring each pair has the same numerical prefix.
   
4. Use Screenshots for Analysis:
   
    Utilize the paired screenshots to identify inconsistencies, such as edge or text inconsistencies.

## To Run the Data Collection Script
1. Setup the Environment:
    - Add the URL of the web application to the script. 
    - Download the required .crx extension file and place it in the specified directory.
2. Collect Data for system preference theme setting Applications:
   - For applications that change themes based on system settings :
   - Run the systempreference.py to capture screenshots in one mode.
   - Once the script complete the process in one mode, the script will stop for few second at that time manually change the system setting to the other mode.
3. Collect Data Using Extensions:
   - run the file data_collection_with_extension.py
   - add the crx file of the extension
4. Run the script data_collection.py to capture the screenshot with toggle button


## Directory Descriptions
1. dawn_bring_clarity:
   -  Contains code that will identify the inconsistency for those application that only support dark mode 
   - extension is used to change the dark mode to light mode 
   - in this phase Screenshots are converted to light mode using the extension.
   - to check the inconsistency from dark mode to light mode use the directory dawn_bring clarity.


2. shadow_reveal_truth:
    - Contain the code to check the inconsistency from light mode to dark mode
    - Applications that natively support both light and dark modes.
    - Applications where themes are converted using the extension.

## To check the inconsistency 

### Edge Inconsistency Analysis
Steps to Check Edge Inconsistency:
1. Open edge_inconsistency.py.
2. Add the path to the original screenshot (light mode or dark mode).
3. Specify the output folder path.
4. Run the script.
5. Output Files:
i. highlighted_light.png: Highlights problematic areas in the original image.
ii. overlay_inconsistency.png: Overlays light and dark mode edges.
   - Green areas indicate problems in dark mode.
   - Red areas indicate problems in light mode.
   - Yellow areas indicate consistent edges.
   
### Text Inconsistency Analysis
   Steps to Check Text Inconsistency:

1. Open text_main.py.
2. Add the paths to the light and dark mode screenshots.
3. Add the path to the OCR output JSON file.
4. Specify the output directory.
5. Run the script. 
6. Output Files:

i. Invisible Text:
    - invisible.png: Side-by-side light and dark mode images, with problematic areas in dark mode highlighted using bounding boxes.
    - invisible.json: Contains details of text content, text color, background color, bounding box area, failure category, and mode.
    - summary.json: A summary of images with problematic areas.
ii. Missing Text:
- missing_text.png: Side-by-side light and dark mode images, with missing text highlighted using bounding boxes.
- missing_text.json: Details of missing text content and mode.
- summary.json: A summary of images with problematic areas.


Full dataset available over here: 