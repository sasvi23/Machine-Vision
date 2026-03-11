# 🤖 Factory Operator UI - Streamlit Application

A user-friendly graphical interface for the vision-guided robotic pick-and-place system with the Dobot MG400.

## Features

✅ **Live Camera Feed** - Capture and display images from your camera
✅ **Object Detection** - Automatically detect objects with color and shape filtering
✅ **Coordinate Mapping** - Convert pixel coordinates to robot workspace coordinates
✅ **Plan/Execute Modes** - Safe planning mode and active execution mode
✅ **Annotated Overlays** - Visual feedback with bounding boxes and coordinates
✅ **Color & Shape Selection** - Filter by red/green/blue/yellow and circle/square
✅ **Status Messages** - Clear feedback on all operations
✅ **Workspace Validation** - Automatic checking of robot workspace limits

## Requirements

- Python 3.8+
- OpenCV (cv2)
- Streamlit
- NumPy
- Dobot MG400 robot (optional, for execution mode)
- Calibration file (calibration.json)

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Ensure calibration is complete:**
   - Run the calibration tool to generate `calibration.json`
   - File should contain homography matrix H and image resolution

## Usage

### Start the Streamlit App

```bash
streamlit run app_streamlit.py
```

The app will open in your default web browser at `http://localhost:8501`

### Workflow

1. **Configure Settings** (Sidebar):
   - Toggle between **Plan** and **Execute** mode
   - Select color filter (any/red/green/blue/yellow)
   - Select shape filter (any/circle/square)
   - Verify calibration is loaded

2. **Capture Image**:
   - Click "📷 Capture / Refresh" button
   - App will capture from camera or load from IMAGE.jpg

3. **Detect Objects**:
   - Click "🔍 Detect Target" button
   - System analyzes image with your selected filters
   - Annotated overlay shows detected objects

4. **Review Results**:
   - See annotated image with target markers
   - Check computed (X, Y) robot coordinates
   - Verify targets are within workspace limits

5. **Execute Pick (Plan/Execute modes)**:
   - **Plan Mode**: Click "🎯 Run Pick" to simulate (no robot movement)
   - **Execute Mode**: Click "🎯 Run Pick" to execute actual robot sequence

## UI Layout

### Left Column (Main Content)
- Camera image display with annotations
- Action buttons (Capture, Detect, Run Pick)
- Real-time image preview

### Right Column (Results)
- Status messages (success/error/warning)
- Detected targets list with:
  - Pixel coordinates (u, v)
  - Robot coordinates (X, Y)
  - Workspace validation status
- Workspace limits reference

### Sidebar (Configuration)
- Mode toggle (Plan/Execute)
- Color filter dropdown
- Shape filter dropdown
- Calibration status & reload
- Camera settings (ID, resolution)

## Safety Features

⚠️ **Plan Mode**: 
- Detects and displays targets
- Computes coordinates
- **Robot does NOT move**
- Safe for testing and planning

⚠️ **Execute Mode**:
- Full system active
- Robot will move on "Run Pick"
- Visual warning displayed
- Clear confirmation workflow

## Keyboard Shortcuts

- `Ctrl+C`: Stop the app
- `R`: Rerun (refresh state)
- `E`: Open settings

## Troubleshooting

### "Calibration file not found"
- Ensure `calibration.json` exists in the same directory
- Run calibration tool first: `python main.py calibrate`

### "Failed to capture image from camera"
- Check camera connection
- Verify camera ID (usually 0)
- Test with: `python -c "import cv2; cap = cv2.VideoCapture(0); cv2.imshow('Test', cap.read()[1])"`

### "No objects detected"
- Check lighting conditions
- Verify object colors match filter ranges
- Objects should be at least 30×30 pixels
- Check `vision/detect.py` for HSV color ranges

### "Objects outside workspace"
- Check robot calibration accuracy
- Verify workspace limits in code
- Objects should be on the table surface within camera view

## Configuration

### Workspace Limits
Edit in `app_streamlit.py`:
```python
WORKSPACE_X_MIN = -50
WORKSPACE_X_MAX = 380
WORKSPACE_Y_MIN = -100
WORKSPACE_Y_MAX = 380
```

### Robot Coordinates
Edit in `app_streamlit.py`:
```python
SAFE_Z = 50       # Height above objects
PICK_Z = -169     # Picking height
DROP_X = 325      # Drop location X
DROP_Y = 235      # Drop location Y
DROP_Z = -79      # Drop height
```

### Camera Settings
Use sidebar controls or edit:
```python
camera_id=0       # Default camera
camera_width=640  # Pixel width
camera_height=480 # Pixel height
```

## Color & Shape Detection

### Supported Colors
- **Red**: `([0, 150, 50], [10, 255, 255])` + `([160, 100, 100], [180, 255, 255])`
- **Green**: `([35, 50, 10], [85, 255, 255])`
- **Blue**: `([90, 100, 50], [140, 255, 255])`
- **Yellow**: `([20, 100, 100], [35, 255, 255])`

### Supported Shapes
- **Circle**: Circularity > 0.8
- **Square**: Circularity ≤ 0.8

Adjust HSV ranges in `vision/detect.py` for your environment.

## Advanced Usage

### Batch Processing Multiple Objects
The system automatically processes all detected objects that:
1. Match color filter (if specified)
2. Match shape filter (if specified)
3. Are within robot workspace limits

Objects are picked sequentially in detection order.

### Loading Custom Images
Place image in workspace as `IMAGE.jpg` and click "Capture / Refresh" to use it instead of camera.

## Performance Notes

- Detection: ~100-200ms per image
- Coordinate mapping: ~10ms
- Robot movement: Depends on distance (2-5 seconds typical)
- UI refresh: ~50ms latency

## Debugging

Enable verbose output by checking logs:
```
streamlit run app_streamlit.py --logger.level=debug
```

## Architecture

```
app_streamlit.py (UI Layer)
    ↓
vision/detect.py (Detection)
    ↓
main.py (Coordinate Mapping)
    ↓
robot/robot_control.py (Execution)
    ↓
dobot_api.py (Hardware)
```

## Integration with CLI

Both the Streamlit UI and CLI (`main.py`) share:
- Same calibration file format
- Same detection pipeline
- Same coordinate mapping
- Same robot control interfaces

Choose the interface that best fits your workflow!

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review system logs (Streamlit console)
3. Verify calibration accuracy: `python calibration/calibrate.py`
4. Test CLI version: `python main.py detect --mode plan`

---

**Last Updated**: March 2026
**Version**: 1.0.0
