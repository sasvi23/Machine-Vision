"""
Machine Vision Factory Operator UI - Streamlit Application
Provides a user-friendly interface for the vision-guided robotic pick-and-place system
"""

import streamlit as st
import cv2
import numpy as np
import os
import json
from datetime import datetime

from vision.detect import Detector
from robot.robot_control import execute_pick_and_place


# ========================================
# CONFIGURATION & SETUP
# ========================================

st.set_page_config(
    page_title="Factory Operator UI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Workspace limits
WORKSPACE_X_MIN = -50
WORKSPACE_X_MAX = 380
WORKSPACE_Y_MIN = -100
WORKSPACE_Y_MAX = 380

SAFE_Z = 50
PICK_Z = -169
DROP_X = 325
DROP_Y = 235
DROP_Z = -79
R = 0


# ========================================
# SESSION STATE INITIALIZATION
# ========================================

def init_session_state():
    """Initialize session state variables"""
    if "mode" not in st.session_state:
        st.session_state.mode = "Plan"
    if "current_image" not in st.session_state:
        st.session_state.current_image = None
    if "annotated_image" not in st.session_state:
        st.session_state.annotated_image = None
    if "detected_objects" not in st.session_state:
        st.session_state.detected_objects = []
    if "filtered_targets" not in st.session_state:
        st.session_state.filtered_targets = []
    if "last_message" not in st.session_state:
        st.session_state.last_message = ""
    if "message_type" not in st.session_state:
        st.session_state.message_type = "info"  # "info", "success", "error", "warning"
    if "H" not in st.session_state:
        st.session_state.H = None
    if "calib_width" not in st.session_state:
        st.session_state.calib_width = None
    if "calib_height" not in st.session_state:
        st.session_state.calib_height = None

init_session_state()


# ========================================
# UTILITY FUNCTIONS
# ========================================

def load_calibration():
    """Load homography matrix from calibration.json"""
    try:
        calibration_path = "calibration.json"
        if not os.path.exists(calibration_path):
            st.session_state.message_type = "error"
            st.session_state.last_message = "❌ Calibration file not found (calibration.json)"
            return False
        
        with open(calibration_path, "r") as f:
            data = json.load(f)
        
        st.session_state.H = np.array(data["H"], dtype=np.float32)
        st.session_state.calib_width = data.get("image_width", 640)
        st.session_state.calib_height = data.get("image_height", 480)
        
        st.session_state.message_type = "success"
        st.session_state.last_message = f"✓ Calibration loaded ({st.session_state.calib_width}x{st.session_state.calib_height})"
        return True
    except Exception as e:
        st.session_state.message_type = "error"
        st.session_state.last_message = f"❌ Error loading calibration: {str(e)}"
        return False


def pixel_to_robot(x_pixel, y_pixel, H):
    """Convert pixel coordinates to robot workspace coordinates"""
    pixel_point = np.array([x_pixel, y_pixel, 1.0], dtype=np.float32)
    robot_point_h = H @ pixel_point
    
    if robot_point_h[2] == 0:
        raise ValueError("Invalid homography normalization (w=0).")
    
    robot_x = robot_point_h[0] / robot_point_h[2]
    robot_y = robot_point_h[1] / robot_point_h[2]
    
    return float(robot_x), float(robot_y)


def is_within_workspace(x, y):
    """Check if coordinates are within robot workspace"""
    return (
        WORKSPACE_X_MIN <= x <= WORKSPACE_X_MAX
        and WORKSPACE_Y_MIN <= y <= WORKSPACE_Y_MAX
    )


def capture_camera_image(camera_id=0, width=640, height=480):
    """Capture image from camera"""
    try:
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            st.session_state.message_type = "error"
            st.session_state.last_message = "❌ Failed to capture image from camera"
            return None
        
        return frame
    except Exception as e:
        st.session_state.message_type = "error"
        st.session_state.last_message = f"❌ Camera error: {str(e)}"
        return None


def resize_to_calibration(frame):
    """Resize frame to match calibration resolution"""
    if st.session_state.calib_width and st.session_state.calib_height:
        current_height, current_width = frame.shape[:2]
        if current_width != st.session_state.calib_width or current_height != st.session_state.calib_height:
            frame = cv2.resize(frame, (st.session_state.calib_width, st.session_state.calib_height))
    return frame


def detect_objects(image, color_filter="any", shape_filter="any"):
    """Detect objects in image using vision pipeline"""
    try:
        detector = Detector()
        detected_objects = detector.find_objects(
            image,
            color_name=color_filter if color_filter != "any" else "any",
            shape_type=shape_filter if shape_filter != "any" else "any",
            show_overlay=False
        )
        
        if not detected_objects:
            st.session_state.message_type = "warning"
            st.session_state.last_message = "⚠️ No objects detected"
            return []
        
        st.session_state.message_type = "info"
        st.session_state.last_message = f"ℹ️ Detected {len(detected_objects)} object(s)"
        return detected_objects
    except Exception as e:
        st.session_state.message_type = "error"
        st.session_state.last_message = f"❌ Detection error: {str(e)}"
        return []


def process_detections(detected_objects):
    """Convert detected objects to robot targets with workspace filtering"""
    robot_targets = []
    
    for obj in detected_objects:
        u, v = obj["pixel_center"]
        try:
            robot_x, robot_y = pixel_to_robot(u, v, st.session_state.H)
            
            if is_within_workspace(robot_x, robot_y):
                robot_targets.append({
                    "pixel_center": (u, v),
                    "robot_coords": (robot_x, robot_y),
                    "shape": obj["Shape"],
                    "color": obj["color"]
                })
        except Exception as e:
            st.session_state.message_type = "error"
            st.session_state.last_message = f"❌ Coordinate conversion error: {str(e)}"
    
    return robot_targets


def bgr_to_rgb(image):
    """Convert BGR image to RGB for Streamlit display"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def draw_annotations(image, targets):
    """Draw target annotations on image (returns BGR by default)"""
    annotated = image.copy()
    
    for target in targets:
        u, v = target["pixel_center"]
        robot_x, robot_y = target["robot_coords"]
        color = target["color"]
        shape = target["shape"]
        
        # Draw circle at center
        cv2.circle(annotated, (int(u), int(v)), 8, (0, 0, 255), -1)
        cv2.circle(annotated, (int(u), int(v)), 12, (0, 255, 255), 2)
        
        # Draw label
        label = f"{color.capitalize()} {shape} ({robot_x:.1f}, {robot_y:.1f})"
        cv2.putText(
            annotated, label,
            (int(u) + 15, int(v) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
            cv2.LINE_AA
        )
    
    return annotated


def execute_robot_sequence(targets, speed=50, accel=50, grip_delay=0.8):
    """Execute pick-and-place sequence (Plan/Execute) with adjustable parameters"""
    if not targets:
        st.session_state.message_type = "warning"
        st.session_state.last_message = "⚠️ No valid targets to execute"
        return False
    
    if st.session_state.mode == "Plan":
        st.session_state.message_type = "info"
        st.session_state.last_message = f"📋 PLAN MODE: {len(targets)} target(s) ready (no robot movement)"
        return True
    
    # Execute mode
    st.session_state.message_type = "info"
    st.session_state.last_message = "🤖 EXECUTE MODE: Starting robot sequence..."
    
    try:
        execute_pick_and_place(
            targets,
            speed_ratio=speed,
            acc_ratio=accel,
            gripper_delay=grip_delay
        )
        st.session_state.message_type = "success"
        st.session_state.last_message = f"✓ Successfully picked and placed {len(targets)} object(s)"
        return True
    except Exception as e:
        st.session_state.message_type = "error"
        st.session_state.last_message = f"❌ Robot execution error: {str(e)}"
        return False


# ========================================
# STREAMLIT UI LAYOUT
# ========================================

# HEADER
st.markdown("# 🤖 Factory Operator UI - Vision-Guided Pick & Place")
st.markdown("---")

# SIDEBAR CONFIGURATION
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # Mode toggle
    mode_col1, mode_col2 = st.columns(2)
    with mode_col1:
        if st.button("📋 Plan", use_container_width=True, type="primary" if st.session_state.mode == "Plan" else "secondary"):
            st.session_state.mode = "Plan"
            st.rerun()
    with mode_col2:
        if st.button("▶️ Execute", use_container_width=True, type="primary" if st.session_state.mode == "Execute" else "secondary"):
            st.session_state.mode = "Execute"
            st.rerun()
    
    st.markdown(f"### Current Mode: **{st.session_state.mode}**")
    
    if st.session_state.mode == "Execute":
        st.warning("⚠️ EXECUTE MODE ACTIVE - Robot will move!", icon="⚠️")
    
    st.markdown("---")
    
    # Filter options
    st.markdown("### 🎯 Filters")
    color_filter = st.selectbox(
        "Color:",
        options=["any", "red", "green", "blue", "yellow"],
        index=0,
        key="color_filter"
    )
    
    shape_filter = st.selectbox(
        "Shape:",
        options=["any", "circle", "square"],
        index=0,
        key="shape_filter"
    )
    
    st.markdown("---")
    
    # Calibration status
    st.markdown("### 📐 Calibration")
    if st.session_state.H is not None:
        st.success(f"✓ Loaded\n{st.session_state.calib_width}×{st.session_state.calib_height}")
    else:
        st.error("Not loaded")
    
    if st.button("🔄 Reload Calibration", use_container_width=True):
        if load_calibration():
            st.session_state.message_type = "success"
            st.session_state.last_message = "✓ Calibration reloaded"
        st.rerun()
    
    st.markdown("---")
    
    # Camera settings
    st.markdown("### 📷 Camera")
    camera_id = st.number_input("Camera ID:", min_value=0, max_value=10, value=0, step=1)
    camera_width = st.number_input("Width (px):", min_value=320, max_value=1920, value=640, step=160)
    camera_height = st.number_input("Height (px):", min_value=240, max_value=1080, value=480, step=120)
    
    st.markdown("---")
    # Robot motion parameters
    st.markdown("### 🤖 Robot Parameters")
    speed_ratio = st.slider("Motion speed (%):", min_value=10, max_value=100, value=50)
    acc_ratio = st.slider("Acceleration (%):", min_value=10, max_value=100, value=50)
    gripper_delay = st.slider("Gripper delay (s):", min_value=0.1, max_value=2.0, value=0.8, step=0.1)


# MAIN CONTENT AREA
main_col1, main_col2 = st.columns([1.5, 1])

with main_col1:
    st.markdown("## 📸 Camera Feed & Results")
    
    # BUTTONS (Action Row)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("📷 Capture / Refresh", use_container_width=True, type="primary"):
            with st.spinner("Capturing image..."):
                # Try to load from file if exists, otherwise capture
                if os.path.exists("IMAGE.jpg"):
                    frame = cv2.imread("IMAGE.jpg")
                    if frame is not None:
                        st.session_state.current_image = frame
                        st.session_state.message_type = "success"
                        st.session_state.last_message = "✓ Loaded from IMAGE.jpg"
                    else:
                        frame = capture_camera_image(camera_id, int(camera_width), int(camera_height))
                        if frame is not None:
                            st.session_state.current_image = frame
                else:
                    frame = capture_camera_image(camera_id, int(camera_width), int(camera_height))
                    if frame is not None:
                        st.session_state.current_image = frame
            st.rerun()
    
    with btn_col2:
        if st.button("🔍 Detect Target", use_container_width=True):
            if st.session_state.current_image is None:
                st.session_state.message_type = "error"
                st.session_state.last_message = "❌ No image captured. Click 'Capture / Refresh' first."
            else:
                with st.spinner("Detecting objects..."):
                    # Resize to calibration resolution
                    processing_image = resize_to_calibration(st.session_state.current_image.copy())
                    
                    # Run detection
                    detected = detect_objects(
                        processing_image,
                        color_filter=color_filter,
                        shape_filter=shape_filter
                    )
                    
                    if detected:
                        st.session_state.detected_objects = detected
                        filtered = process_detections(detected)
                        st.session_state.filtered_targets = filtered
                        
                        if filtered:
                            st.session_state.message_type = "success"
                            st.session_state.last_message = f"✓ Found {len(filtered)} valid target(s) in workspace"
                            st.session_state.annotated_image = draw_annotations(
                                st.session_state.current_image.copy(),
                                filtered
                            )
                        else:
                            st.session_state.message_type = "warning"
                            st.session_state.last_message = "⚠️ Objects detected but outside workspace limits"
            st.rerun()
    
    with btn_col3:
        pick_disabled = st.session_state.mode == "Plan" or len(st.session_state.filtered_targets) == 0
        if st.button(
            "🎯 Run Pick" if not pick_disabled else "🎯 Run Pick (disabled)",
            use_container_width=True,
            disabled=pick_disabled,
            type="primary" if not pick_disabled else "secondary"
        ):
            with st.spinner("Processing robot sequence..."):
                targets_to_execute = [
                    {"robot_coords": t["robot_coords"]} 
                    for t in st.session_state.filtered_targets
                ]
                execute_robot_sequence(
                    targets_to_execute,
                    speed=speed_ratio,
                    accel=acc_ratio,
                    grip_delay=gripper_delay,
                )
            st.rerun()
    
    # IMAGE DISPLAY
    if st.session_state.annotated_image is not None:
        st.image(
            bgr_to_rgb(st.session_state.annotated_image),
            caption="Annotated Detection Results",
            use_column_width=True
        )
    elif st.session_state.current_image is not None:
        st.image(
            bgr_to_rgb(st.session_state.current_image),
            caption="Captured Image (No Detection)",
            use_column_width=True
        )
    else:
        st.info("📸 No image captured yet. Click 'Capture / Refresh' to get started.")


with main_col2:
    st.markdown("## 📊 Results & Status")
    
    # STATUS MESSAGE
    if st.session_state.last_message:
        if st.session_state.message_type == "success":
            st.success(st.session_state.last_message)
        elif st.session_state.message_type == "error":
            st.error(st.session_state.last_message)
        elif st.session_state.message_type == "warning":
            st.warning(st.session_state.last_message)
        else:
            st.info(st.session_state.last_message)
    
    st.markdown("---")
    
    # DETECTED COORDINATES
    if st.session_state.filtered_targets:
        st.markdown("### 🎯 Detected Targets")
        for i, target in enumerate(st.session_state.filtered_targets, 1):
            with st.expander(f"Target {i}: {target['color'].capitalize()} {target['shape']}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Pixel (u, v)",
                        f"({target['pixel_center'][0]}, {target['pixel_center'][1]})"
                    )
                
                with col2:
                    robot_x, robot_y = target['robot_coords']
                    st.metric(
                        "Robot (X, Y)",
                        f"({robot_x:.1f}, {robot_y:.1f})"
                    )
                
                # Workspace status
                in_workspace = is_within_workspace(robot_x, robot_y)
                if in_workspace:
                    st.success("✓ In workspace")
                else:
                    st.error("✗ Outside workspace")
    else:
        st.info("No targets detected yet")
    
    st.markdown("---")
    
    # WORKSPACE LIMITS
    st.markdown("### 📍 Workspace Limits")
    st.text(f"X: [{WORKSPACE_X_MIN}, {WORKSPACE_X_MAX}]")
    st.text(f"Y: [{WORKSPACE_Y_MIN}, {WORKSPACE_Y_MAX}]")
    
    st.markdown("---")
    
    # MODE INDICATOR
    mode_icon = "📋" if st.session_state.mode == "Plan" else "▶️"
    mode_color = "blue" if st.session_state.mode == "Plan" else "red"
    st.markdown(f"### {mode_icon} Mode: {st.session_state.mode}")
    
    if st.session_state.mode == "Plan":
        st.info("Plan mode: Targets detected but robot will NOT move")
    else:
        st.warning("Execute mode: Robot WILL move on 'Run Pick'", icon="⚠️")


# FOOTER
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 0.8em;">
    🤖 Vision-Guided Robotic Pick & Place System | Last updated: """ + datetime.now().strftime("%H:%M:%S") + """
    </div>
    """,
    unsafe_allow_html=True
)

# Load calibration on startup
if st.session_state.H is None:
    load_calibration()
