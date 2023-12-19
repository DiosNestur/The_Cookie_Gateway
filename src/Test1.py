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

def find_image(image_path, threshold=0.8):
    # Load the template image
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
    
    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        # Perform template matching 
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        # Check if the image is found 
        for pt in zip(*loc[::-1]):
            # Image found - you can add additional actions here
            print("Image found on screen")
            cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
            cv2.imshow('Detected', screen)
            
            # Break the loop or return if you only need to find it once
            return
        
        # Display the result (for testing)
        cv2.imshow('Screen', screen_gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(0.5) # add delay in each check (in seconds)
        
    cv2.destroyAllWindows()
    
# Path to the image you are looking for
image_path = ('Images\\Luis.jpg')
print (image_path)
find_image(image_path)

        
            
            