## 📌Overview
This script automates the detection and clicking of golden cookies in **Cookie Clicker**. The script continuously scans your screen for golden cookies, then automatically moves the mouse and clicks them while maintaining high-speed background clicks.

## 📝 Features
- **High-Speed Clicking:** Automatically clicks 50 times per second when no golden cookie is detected.
- **Automatic Golden Cookie Detection:** Uses OpenCV template matching for accurate and reliable detection.
- **Multi-Monitor Support:** Easily configure which monitor to capture.
- **Resolution Scaling Support:** Works with different DPI settings (e.g., 125% scaling) to suit your display.
- **Failsafe Exit:** Press `ESC` at any time to immediately stop the script.

> ⚠️**Warning:** This release has only been tested on a resolution of **1920×1080**. Functionality on other resolutions is not guaranteed.

##  🔧Setup Instructions
Before running the script, **open `golden_cookie_clicks.py`** and configure:
- **Monitor Selection:** Choose the correct monitor for your setup.
- **Resolution Scaling:** Adjust the scaling settings (e.g., 100%, 125%) to match your display.

## 📦Prerequisites
- **Python 3.x**
- Install required libraries:
  ```bash
  pip install pyautogui mss opencv-python numpy keyboard

## 🚀How to Run
- Open a terminal or PowerShell as administrator.
- Launch Cookie Clicker and ensure the main cookie is visible.
- Run the script:
  ```bash
  python3 golden_cookie_clicks.py
  ```
Press ESC to stop the script at any time.
## 🔮Planned Future Improvements
- Wrinkler detection
- Auto buying upgrades
## 💬 Feedback  
Have suggestions or improvements? Feel free to:  
- **Submit a pull request** 
- **Send me a message:**  
  - Reddit: [u/migukau](https://www.reddit.com/user/migukau)  
  - Discord: **migukau**  
