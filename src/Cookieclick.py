import cv2
import numpy as np
import pyautogui
import time
import threading

def click_main_cookie(fixed_center_point, num_clicks):
    for _ in range(num_clicks):
        if fixed_center_point:
            pyautogui.click(fixed_center_point)
            # print("Clicked at fixed point:", fixed_center_point)
        time.sleep(0)  # Intervalo entre clics

def click_golden_cookies(golden_cookies, golden_cookies_paths, threshold):
    while True:
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        for idx, golden_cookie in enumerate(golden_cookies):
            res = cv2.matchTemplate(screen, golden_cookie, cv2.TM_CCOEFF_NORMED)
            if np.any(res >= threshold):
                pt = np.unravel_index(np.argmax(res), res.shape)
                center_point = (pt[1] + golden_cookie.shape[1]//2, pt[0] + golden_cookie.shape[0]//2)
                pyautogui.click(center_point)
                print("Clicked on golden cookie: {} at {}".format(golden_cookies_paths[idx], center_point))
                break  # Break out of golden cookie loop
        time.sleep(0.5)  # Intervalo entre búsquedas

def find_image(main_cookie_path, golden_cookies_paths, threshold=0.9, num_clicks=1000000):
    main_cookie = cv2.imread(main_cookie_path)
    main_cookie = cv2.cvtColor(main_cookie, cv2.COLOR_BGR2RGB)
    w, h = main_cookie.shape[1], main_cookie.shape[0]
    
    golden_cookies = []
    for path in golden_cookies_paths:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        golden_cookies.append(img)

    fixed_center_point = None
    while fixed_center_point is None:
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        res = cv2.matchTemplate(screen, main_cookie, cv2.TM_CCOEFF_NORMED)
        if np.any(res >= threshold):
            pt = np.unravel_index(np.argmax(res), res.shape)
            fixed_center_point = (pt[1] + w//2, pt[0] + h//2)
            print("Fixed center point set at:", fixed_center_point)

    # Crear y empezar los threads
    main_cookie_thread = threading.Thread(target=click_main_cookie, args=(fixed_center_point, num_clicks))
    golden_cookie_thread = threading.Thread(target=click_golden_cookies, args=(golden_cookies, golden_cookies_paths, threshold))

    main_cookie_thread.start()
    golden_cookie_thread.start()

    # Esperar a que ambos threads terminen (opcional)
    main_cookie_thread.join()
    golden_cookie_thread.join()

main_cookie_path = 'Images\\Cookie.PNG'
golden_cookies_paths = ['Images\\goldCookie.PNG'] # 'Images\\BunnyCookie1.PNG' ,'Images\\BunnyCookie2.PNG', 'Images\\BunnyCookie3.PNG', 'Images\\BunnyCookie4.PNG', 'Images\\FortuneCookietry2.PNG'
find_image(main_cookie_path, golden_cookies_paths)