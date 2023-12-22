import cv2
import numpy as np
import pyautogui
import time
import sys

def find_image(image_path, threshold=0.6):
    # Load the template image in color
    template = cv2.imread(image_path)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)  # Convert to RGB
    w, h = template.shape[1], template.shape[0]
    clicked = False  # Add a flag to track whether a click has been made


    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        # Perform template matching 
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        # Check if the image is found and no click has been made yet
        if not clicked and np.any(res >= threshold):
            pt = np.unravel_index(np.argmax(res), res.shape)  # Find the highest correlation point
            click_point = (pt[1] + w//2, pt[0] + h//2)  # Calculate the center point for the click
            pyautogui.click(click_point)  # Perform the click
            print("Image found and clicked at:", click_point)
            clicked = True  # Set the flag to True after the click

        if clicked:
            # Optionally, add a delay after clicking if you want the script to keep running
            time.sleep(2)  # Wait for 2 seconds (or however long you wish)
            # If you want to exit after clicking, uncomment the next two lines
            # cv2.destroyAllWindows()
            # sys.exit()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.5)

# Path to the image you are looking for
image_path = 'Images\\Cookie.PNG'
find_image(image_path)
