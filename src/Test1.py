# Hay que instalar esto para que funcione pip install opencv-python

# #import cv2

# # Load an image
# image = cv2.imread('D:\Descargas\Luis.jpg')

# # Display the image in a window
# cv2.imshow('image', image)

# # Wait for a key press and then close all open windows
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np
import pyautogui
import time
import sys  # Import sys for using sys.exit()

def find_image(image_path, threshold=0.3):
    # Load the template image in color
    template = cv2.imread(image_path)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)  # Convert to RGB
    w, h = template.shape[1], template.shape[0]

    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)  # Convert to RGB

        # Perform template matching 
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        # Check if the image is found 
        found = False
        for pt in zip(*loc[::-1]):
            cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
            found = True
        
        if found:
            print("Image found on screen")
            # Removed the cv2.waitKey(0) to not wait for a key press
            cv2.imshow('Detected', screen)
            cv2.waitKey(1)  # Display the window just for a short moment
            cv2.destroyAllWindows()  # Close all OpenCV windows
            sys.exit()  # Exit the script

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.5)

# Path to the image you are looking for
image_path = 'Images\\Luis.jpg'
find_image(image_path)



        
            
            