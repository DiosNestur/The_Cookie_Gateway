import cv2
import numpy as np
import pyautogui
import time
import sys
import logging



def find_image(image_path, threshold=0.6):
    # Load the template image in color
    template = cv2.imread(image_path)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)  # Convert to RGB
    w, h = template.shape[1], template.shape[0]
    missed_count = 0  # Counter for missed detections
    tolerance = 10
    fixed_center_point = None  # Initialize the fixed center point, we want this so it doesnt break by center missmatching
    num_clicks = 1000000 # How many clicks for loop you want

    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        # Perform template matching 
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # If the image is found for the first time, calculate and fix the center point
        if np.any(res >= threshold) and fixed_center_point is None:
            pt = np.unravel_index(np.argmax(res), res.shape)
            fixed_center_point = (pt[1] + w//2, pt[0] + h//2)  # Calculate the center point
            print("Fixed center point set at:", fixed_center_point)

        # Perform a series of clicks at the fixed center point
        if fixed_center_point:
            for _ in range(num_clicks):
                pyautogui.click(fixed_center_point)
                print("Clicked at fixed point:", fixed_center_point)
                # time.sleep(0)  # Short delay between clicks
            missed_count = 0  # Reset the missed count after clicking
        else:
            missed_count += 1
            print("Image not found on screen. Miss count:", missed_count)
            if missed_count >= tolerance:
                print("Image missed too many times. Exiting.")
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

        time.sleep(0.5)  # Check for the image every half second

# Path to the image you are looking for
image_path = 'Images\\Cookie.PNG'
find_image(image_path)
