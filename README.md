# Virtual Mouse Controller with Voice Commands

A Python-based **AI Virtual Mouse** system that uses **hand gestures** and **voice commands** to control mouse movements, clicks, and scrolling providing real-time touch-free experience. Built using OpenCV, MediaPipe, and speech recognition libraries.

## Features

- Real-time hand tracking using webcam
- Index finger controls mouse cursor
- Finger gestures to perform click, scroll, drag
- Voice commands like “click”, “scroll down”, “stop”, etc.
- OpenCV window showing live feedback
- Smart smoothing and edge clamping for accurate movement
- Idle detection to save CPU

## Gesture Controls

| Gesture               | Action                    |
|-----------------------|---------------------------|
| Index finger up       | Move mouse cursor         |
| Index + Middle close  | Left Click                |
| Thumb + Index close   | Scroll (up/down)          |
| All 5 fingers up      | Pause movement            |
| "Drag"/"Release" voice| Enable/disable drag mode  |


## Voice Commands

| Command             | Action                  |
|---------------------|-------------------------|
| `click`             | Left click              |
| `scroll down`       | Scroll the page down    |
| `scroll up`         | Scroll the page up      |
| `drag`              | Enable mouse drag       |
| `release`           | Release mouse drag      |
| `next` / `previous` | Slide navigation        |
| `sleep`             | Mute voice input        |
| `wake` / `start`    | Resume voice input      |
| `stop`              | Exit the application    |


## Requirements

Install required libraries using pip:

```bash
pip install opencv-python mediapipe autopy pyautogui SpeechRecognition numpy
```

## How to run
``` bash
python VirtualMouse.py
```

## Notes

1. Make sure your microphone is enabled and accessible.
2. If webcam doesn't work, try changing cam_index = 0 to 1 or 2.
3. Works best in well-lit environments.


