# 🎯 Factory Operator UI - User Guide

Complete walkthrough for operating the vision-guided robotic pick-and-place system.

## Getting Started in 3 Steps

### Step 1: Installation
```bash
# Navigate to the project directory
cd Machine_Vision

# Install dependencies
pip install -r requirements.txt

# OR use the quick start script
python run_ui.py
```

### Step 2: Prepare Calibration
```bash
# Generate calibration.json if you haven't already
python main.py calibrate
```

### Step 3: Launch the UI
```bash
# Option A: Using quick start script
python run_ui.py

# Option B: Direct command
streamlit run app_streamlit.py
```

The application will open at `http://localhost:8501`

---

## UI Overview

### 🎨 Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 Factory Operator UI - Vision-Guided Pick & Place            │
├──────────────────────┬──────────────────────────────────────────┤
│                      │                                          │
│  ⚙️ SIDEBAR          │  📸 MAIN CONTENT AREA                  │
│  ──────              │  ─────────────────────                 │
│  • Mode Toggle       │  • Camera Feed                          │
│  • Plan / Execute    │  • Detection Results                    │
│  • Color Filter      │                                          │
│  • Shape Filter      │            📸 IMAGE                     │
│  • Calibration       │          [Display Area]                │
│                      │                                          │
│                      ├──────────────────────────────────────────┤
│  📐 Calibration      │  📊 RESULTS PANEL                       │
│  ✓ Loaded            │  ──────────────────                     │
│  640×480             │  • Status Messages                      │
│                      │  • Target Coordinates                   │
│  📷 Camera           │  • Workspace Validation                 │
│  ID: 0               │  • Mode Indicator                       │
│  640 × 480           │                                          │
│                      │                                          │
└──────────────────────┴──────────────────────────────────────────┘
```

---

## Detailed Workflow

### 1️⃣ Configure Your Session

**Sidebar → Mode Selection**

```
┌─────────────────────┐
│   📋 Plan           │   ← Safe test mode
│   ▶️ Execute        │   ← Active operation
└─────────────────────┘
```

- **Plan Mode** (Default):
  - ✓ Detects objects
  - ✓ Computes coordinates
  - ✗ Robot does NOT move
  - Perfect for testing

- **Execute Mode**:
  - ✓ Detects objects
  - ✓ Computes coordinates
  - ✓ Robot MOVES
  - ⚠️ Be cautious!

**Sidebar → Filters**

```
Color:   [any ▼]      (red, green, blue, yellow)
Shape:   [any ▼]      (circle, square)
```

Set filters to narrow down detection:
- `Color: red, Shape: circle` → Pick only red circles
- `Color: any, Shape: square` → Pick any colored squares
- `Color: blue, Shape: any` → Pick blue objects of any shape

**Sidebar → Robot Parameters**

```
Speed:      [50% slider]   (motion speed)
Acceleration:[50% slider]  (motion acceleration)
Gripper delay:[0.8s slider] (pause after open/close)
```

Adjust these values before running a pick sequence to make the robot faster or slower. Lower delays and higher speed/accel will shorten the time between picks.

### 2️⃣ Capture Image

**Main Area → Capture / Refresh Button**

```
┌─────────────────────────────────────┐
│ 📷 Capture / Refresh                │  ← Click to capture
└─────────────────────────────────────┘
```

The system will:
1. First check for `IMAGE.jpg` in the project folder
2. If not found, capture from your camera
3. Auto-resize to calibration resolution
4. Display in the image area

**Status Feedback:**
```
✓ Loaded from IMAGE.jpg
```
or
```
✓ Captured from camera (ID:0)
```

### 3️⃣ Detect Objects

**Main Area → Detect Target Button**

```
┌─────────────────────────────────────┐
│ 🔍 Detect Target                    │  ← Click to analyze
└─────────────────────────────────────┘
```

The detection engine:
1. Analyzes image colors and shapes
2. Applies selected filters
3. Computes pixel centers (u, v)
4. Converts to robot coordinates (X, Y)
5. Validates workspace limits

**Expected Output:**

```
ℹ️ Detected 3 object(s)
✓ Found 3 valid target(s) in workspace
```

or

```
⚠️ Objects detected but outside workspace limits
```

### 4️⃣ Review Results

**Right Panel → Detected Targets**

Each target shows:

```
▼ Target 1: Red Circle
  ├─ Pixel (u, v):      (245, 180)
  ├─ Robot (X, Y):      (125.3, 98.7)
  └─ Status:            ✓ In workspace

▼ Target 2: Blue Square
  ├─ Pixel (u, v):      (420, 310)
  ├─ Robot (X, Y):      (287.2, 156.4)
  └─ Status:            ✓ In workspace
```

**Understanding Coordinates:**
- **Pixel (u, v)**: Position in the camera image
  - u = horizontal (0 = left edge)
  - v = vertical (0 = top edge)
- **Robot (X, Y)**: Position in robot workspace
  - X = forward/backward
  - Y = left/right
  - Z = height (not shown, controlled by software)

### 5️⃣ Execute (Plan or Execute Mode)

**Main Area → Run Pick Button**

```
┌─────────────────────────────────────┐
│ 🎯 Run Pick (disabled if Plan Mode) │
└─────────────────────────────────────┘
```

**In PLAN Mode:**
```
Button is enabled but dimmed
Click → 📋 PLAN MODE: 3 target(s) ready (no robot movement)
```

**In EXECUTE Mode:**
```
Button is bright and active
Click → 🤖 EXECUTE MODE: Starting robot sequence...

Robot will:
1. Move to position above first object (at SAFE_Z height)
2. Lower down to PICK_Z height
3. Close gripper (DO1 = 1)
4. Lift up to SAFE_Z
5. Move to drop position (DROP_X, DROP_Y, DROP_Z)
6. Open gripper (DO1 = 0)
7. Return to ready position
[Repeat for each object]

Final status:
✓ Successfully picked and placed 3 object(s)
```

---

## 🔧 Camera Configuration

On the sidebar, you can adjust:

```
📷 Camera
├─ Camera ID:   0      (0 = primary camera)
├─ Width (px):  640    (320-1920)
└─ Height (px): 480    (240-1080)
```

**Common Values:**
- 640×480: Good balance, matches calibration
- 1280×720: HD, more detail
- 320×240: Low res, faster

**Camera ID:**
- `0` = primary/default camera
- `1` = secondary camera (if available)
- Check what's available: `python -c "import cv2; cap = cv2.VideoCapture(0)"`

---

## ⚠️ Safety Workflow

### Recommended Sequence

```
1. Start in PLAN MODE (default)
   └─ Test detection, coordinate mapping
   
2. Verify results visually
   └─ Check annotated image
   └─ Confirm (X,Y) coordinates make sense
   
3. Switch to EXECUTE MODE
   └─ Clear the workspace first!
   └─ Ensure gripper is functional
   
4. Run Pick with caution
   └─ Watch robot movement
   └─ Have emergency stop ready
   
5. Inspect results
   └─ Verify gripper function
   └─ Check object placement
```

### Emergency Stop

- **Keyboard**: Press `Ctrl+C` in terminal
- **Streamlit**: Click "Stop running" (top right)
- **Physical**: Have manual robot control available

---

## 📊 Understanding Status Messages

### Success Messages ✓
```
✓ Calibration loaded
✓ Found 3 valid target(s) in workspace
✓ Successfully picked and placed 3 object(s)
✓ Loaded from IMAGE.jpg
```
→ Everything is working as expected

### Info Messages ℹ️
```
ℹ️ Detected 5 object(s)
ℹ️ PLAN MODE: 3 target(s) ready (no robot movement)
ℹ️ EXECUTE MODE: Starting robot sequence...
```
→ Informational, normal operation

### Warning Messages ⚠️
```
⚠️ EXECUTE MODE ACTIVE - Robot will move!
⚠️ Objects detected but outside workspace limits
⚠️ No objects detected
```
→ Something needs attention but not critical

### Error Messages ❌
```
❌ Calibration file not found
❌ Failed to capture image from camera
❌ No image captured. Click 'Capture / Refresh' first.
❌ Detection error: [error details]
❌ Robot execution error: [error details]
```
→ Operation failed, troubleshooting needed

---

## 🔍 Detecting Different Objects

### By Color

The system recognizes:
- **Red**: Bright red objects (HSV ~0° or ~180°)
- **Green**: Bright green objects (HSV ~120°)
- **Blue**: Bright blue objects (HSV ~240°)
- **Yellow**: Bright yellow objects (HSV ~60°)

**To detect objects:**
1. Ensure good lighting
2. Objects should be clearly colored
3. Use dropdown: `Color: red` (for example)
4. Click "Detect Target"

### By Shape

The system distinguishes:
- **Circle**: Round objects (Circularity > 0.8)
- **Square**: Rectangular/angular objects (Circularity ≤ 0.8)

**To detect by shape:**
1. Use dropdown: `Shape: circle` (for example)
2. Click "Detect Target"
3. Works regardless of color

### Combined (Color + Shape)

Select both filters:
```
Color:  [blue ▼]
Shape:  [circle ▼]
```

Result: Only blue circles are detected

---

## 📐 Understanding Workspace Limits

The right panel shows:

```
📍 Workspace Limits
X: [-50, 380]
Y: [-100, 380]
```

This means:
- Objects with X outside [-50, 380] are invalid
- Objects with Y outside [-100, 380] are invalid
- Robot cannot physically reach outside these bounds

**If targets are outside workspace:**
```
⚠️ Objects detected but outside workspace limits
```

**Solutions:**
1. Place objects closer to table center
2. Adjust camera angle
3. Recalibrate camera to table mapping
4. Check `main.py` for workspace constants

---

## 🐛 Troubleshooting

### Problem: "Calibration file not found"

✗ Error:
```
❌ Calibration file not found (calibration.json)
```

✓ Solution:
```bash
# Run calibration tool
python main.py calibrate

# Follow prompts to select calibration points
# This will create calibration.json

# Then reload calibration:
# Click "🔄 Reload Calibration" in sidebar
```

### Problem: "Failed to capture image from camera"

✗ Error:
```
❌ Failed to capture image from camera
```

✓ Solutions:
1. Check camera connection
2. Try different camera ID (0, 1, 2...)
3. Close other applications using camera
4. Test with: `python test_camera.py`

**test_camera.py:**
```python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    print("✓ Camera works!")
    cv2.imshow("Test", frame)
    cv2.waitKey(0)
else:
    print("✗ Camera failed")
cap.release()
```

### Problem: "No objects detected"

✗ Status:
```
⚠️ No objects detected
```

✓ Check:
1. **Lighting**: Are objects well-lit and visible?
2. **Color**: Do they match the HSV ranges?
3. **Size**: Are they at least 30×30 pixels?
4. **Contrast**: Do they stand out from background?

✓ Debug:
```python
# In vision/detect.py, check HSV ranges
# Try manual HSV detection:

import cv2
import numpy as np

img = cv2.imread("IMAGE.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Try to isolate red
lower = np.array([0, 150, 50])
upper = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower, upper)

cv2.imshow("Red mask", mask)
cv2.waitKey(0)

# If mask is mostly black, colors don't match
# Adjust ranges in detect.py
```

### Problem: "Objects outside workspace"

✗ Status:
```
⚠️ Objects detected but outside workspace limits
```

✓ Reason: Objects detected but robot cannot reach them

✓ Solutions:
1. Physically move objects into camera view
2. Place objects on table surface only
3. Check calibration accuracy
4. Verify workspace limits match your hardware

### Problem: "No image captured"

✗ Error:
```
❌ No image captured. Click 'Capture / Refresh' first.
```

✓ Solution: Click "📷 Capture / Refresh" button first!

### Problem: Robot won't move (Execute mode)

✗ Status: Button is active but robot doesn't move

✓ Check:
1. Robot is powered on
2. Robot IP address is correct: `192.168.1.6`
3. Network connection established
4. No safety errors on robot
5. Check robot manual for error codes

---

## 📝 Advanced Tips

### Using Batch Images

Instead of live camera:
1. Save image as `IMAGE.jpg` in project directory
2. Click "📷 Capture / Refresh"
3. App will load IMAGE.jpg automatically

### Testing Detection Without Robot

1. Stay in PLAN MODE
2. Test with different images
3. Verify coordinate calculation
4. No risk of unintended robot movement

### Optimizing Color Detection

HSV values are in `vision/detect.py`:

```python
self.colors = {
    "red": [
        ([0, 150, 50], [10, 255, 255]),      # Lower red range
        ([160, 100, 100], [180, 255, 255])   # Upper red range
    ],
    "green": [
        ([35, 50, 10], [85, 255, 255])
    ],
    # ... more colors
}
```

**HSV Ranges:**
- **H (Hue)**: 0-180 (color wheel)
  - Red: ~0° and ~180°
  - Green: ~120°
  - Blue: ~240°
- **S (Saturation)**: 0-255 (color intensity)
- **V (Value)**: 0-255 (brightness)

Adjust ranges for your specific lighting!

### Gripping Parameters

Edit in `robot_control.py`:

```python
SAFE_Z = 50       # Height above object for clearance
PICK_Z = -169     # Height at which to grip (table height)
DROP_X = 325      # Where to drop (X position)
DROP_Y = 235      # Where to drop (Y position)
DROP_Z = -79      # Drop height
```

### Performance Optimization

If detection is slow:
1. Reduce image resolution (480p instead of 720p)
2. Increase minimum object area in `detect.py`
3. Reduce morphological kernel size
4. Use specific color filter instead of "any"

---

## 📚 Reference

### File Structure
```
Machine_Vision/
├── app_streamlit.py        ← Main UI file
├── main.py                 ← CLI interface
├── run_ui.py               ← Quick start script
├── requirements.txt        ← Dependencies
├── STREAMLIT_README.md     ← Technical docs
├── USER_GUIDE.md           ← This file
├── calibration.json        ← Camera calibration
├── .streamlit/
│   └── config.toml         ← Streamlit settings
├── vision/
│   ├── __init__.py
│   └── detect.py           ← Object detection
├── robot/
│   ├── __init__.py
│   ├── robot_control.py    ← Pick & place sequence
│   └── dobot_controller.py ← Robot communication
├── calibration/
│   └── calibrate.py        ← Calibration tool
└── outputs/                ← Generated images
```

### Common Commands

```bash
# Start UI
streamlit run app_streamlit.py

# Quick start
python run_ui.py

# CLI testing
python main.py detect --mode plan

# Calibration
python main.py calibrate

# CLI with filters
python main.py detect --color red --shape circle --mode plan
```

### Keyboard Shortcuts (in Streamlit)

- `Ctrl+C`: Stop app
- `R`: Rerun entire app
- `E`: Open sidebar
- `D`: Debug mode

---

## 🎓 Learning Path

1. **Start Here**: Read this guide sections 1-3
2. **Test Locally**: Configure camera, capture images
3. **Learn Detection**: Understand color/shape filters
4. **Safe Practice**: Test extensively in PLAN MODE
5. **Execute**: Switch to EXECUTE mode when confident
6. **Troubleshoot**: Use debugging section as needed

---

## ❓ FAQ

**Q: Can I use multiple cameras?**
A: Yes! Change Camera ID in sidebar (0, 1, 2, etc.)

**Q: How do I calibrate?**
A: Run `python main.py calibrate` and follow prompts

**Q: Can I pick multiple objects?**
A: Yes! All detected objects in workspace are processed sequentially

**Q: What if objects are different colors?**
A: Use `Color: any` to detect all colors, or set specific color

**Q: How fast is picking?**
A: Typically 2-5 seconds per object depending on distance

**Q: Can I change drop location?**
A: Edit `DROP_X`, `DROP_Y`, `DROP_Z` in `app_streamlit.py`

**Q: Is Plan mode truly safe?**
A: Yes! In Plan mode, robot never receives movement commands

---

## 📞 Support & Issues

If you encounter problems:
1. Check this guide's troubleshooting section
2. Review system logs (visible in Streamlit console)
3. Test with CLI: `python main.py detect --mode plan`
4. Check hardware connections and robot power
5. Verify calibration: `python main.py calibrate`

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Status**: Ready for production use ✓

