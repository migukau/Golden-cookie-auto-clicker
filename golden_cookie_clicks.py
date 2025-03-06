import pyautogui
import time
import cv2
import numpy as np
import keyboard  # To allow stopping the script
import threading
import mss

# Monitor settings:
"""
Monitor settings are used to determine the region dimensions and scaling factor. 
They are case-specific and may need to be adjusted.

The index of the monitors in the mss library depends on how the operating system enumerates them. 
For example, on Windows, the primary monitor is usually 1, while on Linux it is 0.

On windows, go to display settings to check the monitor index and the scale of the monitor where cookie clicker is running.
Usually the scaling value is 125% for laptops.
"""
#################### CHANGE THESE VALUES ####################
# On windows, go to display settings to check the monitor index and the scale of the monitor where cookie clicker is running
monitor = 1
scaling = 1.25 # 125% scaling in this case
#############################################################

with mss.mss() as sct:
    monitor_region = sct.monitors[monitor]
    left = monitor_region["left"]

# Global events for thread communication
pause_clicking_event = threading.Event()  # When set, pauses the fast clicking
stop_event = threading.Event()            # When set, all threads will exit

# Global variables for main cookie position
main_x = None
main_y = None

# Interval between each screenshot for the golden cookie detector (seconds)
poll_interval = 2

def main_cookie_detector():
    global main_x, main_y
    
    main_cookie_image = "main_cookie.png"  # Template image file
    template = cv2.imread(main_cookie_image)
    if template is None:
        print("Error: Main cookie template image not found.")
        stop_event.set()
        return
    
    try:
        with mss.mss() as sct:
            monitor_region = sct.monitors[monitor]  # sct.monitors[0] is all monitors combined
            sct_img = sct.grab(monitor_region)
            screen_np = np.array(sct_img)
            screen = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2BGR)
        
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.4:  # Main cookie detected
            x, y = max_loc
            
            template_center_x = template.shape[1] // 2
            template_center_y = template.shape[0] // 2
            
            main_x = left + (x + template_center_x) / scaling
            main_y = (y + template_center_y) / scaling
                        
            pyautogui.moveTo(main_x, main_y)
            
    except Exception as e:
        print(f"Error in main cookie detector: {e}")


def constant_clicker():
    while not stop_event.is_set():
        if not pause_clicking_event.is_set():
            try:
                pyautogui.click(clicks=100, interval=0.008, x=main_x, y=main_y)
            except Exception as e:
                print(f"Click error: {e}")
        else:
            time.sleep(0.01)

def golden_cookie_detector():
    """
    Continuously scans for the golden cookie.
    When found, pauses fast clicking, moves to the cookie,
    clicks, then returns to the original position
    and resumes fast clicking.
    """
    cookie_image = "golden_cookie.png"  # Template image file
    template = cv2.imread(cookie_image)
    if template is None:
        print("Error: Golden cookie template image not found.")
        stop_event.set()
        return
    
    # Convert the template from BGRA to BGR if it has an alpha channel
    if template.shape[2] == 4:  # Check if the image has an alpha channel
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        print("Converted template image to BGR")

    while not stop_event.is_set():
        try:
            with mss.mss() as sct:
                monitor_region = sct.monitors[monitor]
                scaled_monitor = {
                    "left": monitor_region["left"],
                    "top": monitor_region["top"],
                    "width": int(monitor_region["width"] * scaling),
                    "height": int(monitor_region["height"] * scaling)
                }
                sct_img = sct.grab(scaled_monitor)
                screen_np = np.array(sct_img)
                screen = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2BGR)
                cv2.imwrite(f"screenshot.png", screen)
            
            result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            
            if max_val > 0.44:  # Cookie detected with sufficient confidence
                # Pause the constant clicking thread
                pause_clicking_event.set()
                
                x, y = max_loc
                template_center_x = template.shape[1] // 2
                template_center_y = template.shape[0] // 2
                
                # Calculate final coordinates; apply scaling only to relative values
                final_x = left + (x + template_center_x) / scaling
                final_y = (y + template_center_y) / scaling

                pyautogui.click(final_x, final_y)
                print(f"Cookie detected and clicked at: ({final_x}, {final_y}) with confidence {max_val:.2f}")
                
                time.sleep(0.1)  # Pause briefly after clicking
                pyautogui.moveTo(main_x, main_y)
                
                # Resume fast clicking
                pause_clicking_event.clear()
            
            # print(f"Cookie not found. Confidence: {max_val:}")
            time.sleep(poll_interval) # Wait before next detection
        except Exception as e:
            print(f"Error in golden cookie detector: {e}")

if __name__ == "__main__":
    print("Starting cookie clicker script...")
    
    main_cookie_detector()
    
    
    
    if main_x and main_y:
        print("Main cookie detected at:", main_x, main_y)
                    
        # Start threads for constant clicking and cookie detection
        click_thread = threading.Thread(target=constant_clicker)
        detect_thread = threading.Thread(target=golden_cookie_detector)

        click_thread.start()
        detect_thread.start()

        print(f"Press ESC to stop the script. (Wait {poll_interval} seconds)")
        # Wait for ESC key press. When pressed, signal both threads to stop.
        keyboard.wait("esc")
        stop_event.set()
        pause_clicking_event.set()  # Ensure constant_clicker isn't stuck in a paused state

        click_thread.join()
        detect_thread.join()
        print("Script terminated.")
    else:
        print("Main cookie not found. Exiting.")