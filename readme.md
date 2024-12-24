Requirement 

Python requirement
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
2. Collect Data for Theme-Based Applications:
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
