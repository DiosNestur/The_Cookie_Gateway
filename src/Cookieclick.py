import cv2
import numpy as np
import pyautogui
import time
import threading

# Crear un bloqueo para controlar el acceso al mouse
mouse_lock = threading.Lock()

def click_main_cookie(fixed_center_point, num_clicks):
    for _ in range(num_clicks):
        if fixed_center_point:
            with mouse_lock:  # Adquirir el bloqueo antes de hacer clic
                pyautogui.click(fixed_center_point)
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
                with mouse_lock:
                    pyautogui.click(center_point)
                print("Clicked on golden cookie: {} at {}".format(golden_cookies_paths[idx], center_point))
                break  # Break out of golden cookie loop
        time.sleep(0.5)  # Intervalo entre búsquedas

def click_fortune_cookie(color_rgb, color_tolerance, threshold):
    lower_bound = np.array([max(0, c - color_tolerance) for c in color_rgb])
    upper_bound = np.array([min(255, c + color_tolerance) for c in color_rgb])

    while True:
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        mask = cv2.inRange(screen, lower_bound, upper_bound)
        coordinates = cv2.findNonZero(mask)

        if coordinates is not None:
            x, y = coordinates[0][0]
            with mouse_lock:  # Adquirir el bloqueo antes de hacer clic
                pyautogui.click(x, y)
                print("Clicked on fortune cookie at", (x, y))
            break  # Salir después del primer clic
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

    # Color RGB de la galleta de la fortuna (convertido de #acdf00)
    fortune_cookie_color = (172, 223, 0)
    color_tolerance = 10
    
    # Crear y empezar los threads
    main_cookie_thread = threading.Thread(target=click_main_cookie, args=(fixed_center_point, num_clicks))
    golden_cookie_thread = threading.Thread(target=click_golden_cookies, args=(golden_cookies, golden_cookies_paths, threshold))
    fortune_cookie_thread = threading.Thread(target=click_fortune_cookie, args=(fortune_cookie_color, color_tolerance, 0.9))

    main_cookie_thread.start()
    golden_cookie_thread.start()
    fortune_cookie_thread.start()

    # Esperar a que todos los threads terminen (opcional)
    main_cookie_thread.join()
    golden_cookie_thread.join()
    fortune_cookie_thread.join()

main_cookie_path = 'Images\\Cookie.PNG'
golden_cookies_paths = ['Images\\goldCookie.PNG', 'Images\\BunnyCookie1.PNG', 'Images\\BunnyCookie2.PNG', 'Images\\BunnyCookie3.PNG', 'Images\\BunnyCookie4.PNG', 'Images\\FortuneCookietry2.PNG']
find_image(main_cookie_path, golden_cookies_paths)
