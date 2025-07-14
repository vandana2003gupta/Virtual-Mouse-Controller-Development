# Virtual Mouse Controller Using Hand Gestures

This Python-based project allows users to control their mouse cursor using hand gestures captured through a webcam. 
It uses computer vision techniques with OpenCV and MediaPipe to track finger movements and simulate mouse actions like movement, left-click, and right-click.


## Features

- Real-time hand tracking using webcam
- Cursor movement based on index finger position
- Left-click with index and middle finger gesture
- Right-click and scroll functionality (optional extension)
- Smooth and responsive user experience


## Technologies Used

- **Python**
- **OpenCV** – for real-time video capture and image processing
- **MediaPipe** – for accurate hand landmark detection
- **PyAutoGUI** – for controlling the system mouse


## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vandana2003gupta/Virtual-Mouse-Controller-Development.git

2. **Navigate to the project folder:**
   cd Virtual-Mouse-Controller-Development

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Run:**
   Make sure your webcam is connected. Then run the following command:
   python VirtualMouse.py
   
6. **Use hand gestures in front of the webcam to move and click the mouse**

| Gesture                          | Action            |
|----------------------------------|-------------------|
| 🖐️ Index finger up              | Move the cursor   |
| ✌️ Index + Middle fingers up    | Left click        |
| 🤞 Index + Middle pinch gesture | Right click       |
| ✋ All fingers extended (swipe up/down) | Scroll up/down     |

> 👆 Ensure your hand is clearly visible to the webcam and gestures are stable for accurate detection.



