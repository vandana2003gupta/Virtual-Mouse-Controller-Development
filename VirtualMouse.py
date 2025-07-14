"""
VirtualMouse.py – terminal / OpenCV window version
Run with:  python VirtualMouse.py
"""

import cv2, numpy as np, autopy, pyautogui, time, threading, atexit, sys
import pyttsx3, speech_recognition as sr
import HandTrackingModule as htm

# SETTINGS 
wCam, hCam = 640, 480
frameR = 70
smoothening = 7
idle_thresh = 15
cam_index = 0            # change if your camera is on index 1

# HELPERS 
def clamp(val, lo, hi):
    """Clamp a number into the closed interval [lo, hi]."""
    return max(lo, min(val, hi))

def open_cam(idx=0):
    """Try DirectShow → MSMF → default backend until a camera opens."""
    for backend in (cv2.CAP_DSHOW, cv2.CAP_MSMF, None):
        cap = cv2.VideoCapture(idx) if backend is None else cv2.VideoCapture(idx, backend)
        if cap.isOpened():
            return cap
    return None

# INITIALISE 
cap = open_cam(cam_index)
if not cap:
    sys.exit("Could not open webcam. Check privacy settings or index.")

cap.set(3, wCam); cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
screen_w, screen_h = autopy.screen.size()

engine      = pyttsx3.init()
recognizer  = sr.Recognizer()

running   = True
voice_on  = True
drag_mode = False
plocX = plocY = clocX = clocY = 0
last_seen = time.time()
pTime     = 0

def cleanup():
    cap.release()
    cv2.destroyAllWindows()
atexit.register(cleanup)

# VOICE THREAD
def speak(text):
    engine.say(text); engine.runAndWait()

def listen():
    with sr.Microphone() as src:
        try:
            audio = recognizer.listen(src, timeout=4, phrase_time_limit=5)
            return recognizer.recognize_google(audio).lower()
        except Exception:
            return ""

def voice_loop():
    global running, voice_on, drag_mode
    while running:
        if not voice_on:
            time.sleep(0.3); continue
        cmd = listen()
        if not cmd: continue
        print("Voice:", cmd)

        if "stop"  in cmd: speak("Stopping"); running = False; break
        elif "sleep" in cmd: voice_on = False; speak("Sleeping")
        elif "wake"  in cmd or "start" in cmd: voice_on = True; speak("Awake")
        elif "click" in cmd: pyautogui.click()
        elif "scroll down" in cmd or "scroll" in cmd: pyautogui.scroll(-200)
        elif "scroll up"   in cmd: pyautogui.scroll(200)
        elif "drag" in cmd: drag_mode = True; pyautogui.mouseDown(); speak("Drag on")
        elif "release" in cmd: drag_mode = False; pyautogui.mouseUp(); speak("Drag off")
        elif "next" in cmd: pyautogui.press("right")
        elif "previous" in cmd: pyautogui.press("left")

threading.Thread(target=voice_loop, daemon=True).start()

#  MAIN LOOP 
while running:
    ok, img = cap.read()
    if not ok: continue
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:
        last_seen = time.time()
        x1, y1 = lmList[8][1:]
        fingers = detector.fingersUp()

        cv2.rectangle(img, (frameR, frameR),
                      (wCam-frameR, hCam-frameR), (255,0,255), 2)

        # Move: only index finger up
        if fingers == [0,1,0,0,0]:
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, screen_w))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, screen_h))
            clocX = plocX + (x3-plocX)/smoothening
            clocY = plocY + (y3-plocY)/smoothening

            # 🛡 Clamp to screen bounds to avoid ValueError
            safeX = clamp(screen_w - clocX, 0, screen_w - 1)
            safeY = clamp(clocY, 0, screen_h - 1)
            autopy.mouse.move(safeX, safeY)

            if drag_mode: pyautogui.mouseDown()
            else:         pyautogui.mouseUp()

            cv2.circle(img, (x1, y1), 12, (255,0,255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Click
        if fingers[1] and fingers[2]:
            length, img, _ = detector.findDistance(8, 12, img)
            if length < 40: pyautogui.click()

        # Scroll
        if fingers[0] and fingers[1] and not fingers[2]:
            length, *_ = detector.findDistance(4, 8, img, draw=False)
            if length < 40:      pyautogui.scroll(-30)
            elif length > 70:    pyautogui.scroll(30)

        # Five‑finger pause
        if fingers == [1,1,1,1,1]:
            speak("Pausing movement")
            time.sleep(1)

    elif time.time() - last_seen > idle_thresh:
        time.sleep(0.1)   # idle → lighten CPU

    # FPS overlay
    cTime = time.time()
    fps = 1/(cTime - pTime + 1e-5); pTime = cTime
    cv2.putText(img, f"FPS:{int(fps)}", (10,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF in (27, ord('q')):
        running = False

cleanup()
