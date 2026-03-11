import argparse
import cv2
import numpy as np
import os
import json

from vision.detect import Detector
from robot.robot_control import execute_pick_and_place

# -------------------------------
# Workspace limits (adjust if needed)
# -------------------------------
WORKSPACE_X_MIN = -50
WORKSPACE_X_MAX = 380
WORKSPACE_Y_MIN = -100
WORKSPACE_Y_MAX = 380

# -------------------------------
# Pixel → Robot transformation
# -------------------------------
def pixel_to_robot(x_pixel, y_pixel, H):
    pixel_point = np.array([x_pixel, y_pixel, 1.0], dtype=np.float32)
    robot_point_h = H @ pixel_point

    if robot_point_h[2] == 0:
        raise ValueError("Invalid homography normalization (w=0).")

    robot_x = robot_point_h[0] / robot_point_h[2]
    robot_y = robot_point_h[1] / robot_point_h[2]

    return float(robot_x), float(robot_y)


def is_within_workspace(x, y):
    return (
        WORKSPACE_X_MIN <= x <= WORKSPACE_X_MAX
        and WORKSPACE_Y_MIN <= y <= WORKSPACE_Y_MAX
    )


def main():
    parser = argparse.ArgumentParser(description="Vision-to-Robot Pipeline")
    parser.add_argument("--mode", choices=["plan", "execute"], default="plan")
    parser.add_argument("--color", type=str, default="any")
    parser.add_argument("--shape", type=str, default="any")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--image", type=str, help="Path to input image file")
    args = parser.parse_args()

    print("\n--- Vision-to-Robot Pipeline Started ---")
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        calibration_path = os.path.join(BASE_DIR, "calibration.json")
        with open(calibration_path, "r") as f:
            data = json.load(f)

        H = np.array(data["H"], dtype=np.float32)
        calib_width = data["image_width"]
        calib_height = data["image_height"]

        print("Loaded homography matrix:")
        print(H)
        print(f"Calibration resolution: {calib_width} x {calib_height}")

    except Exception as e:
        print(f"Error loading calibration: {e}")
        return

    if args.image:
        print(f"Loading image from: {args.image}")
        frame = cv2.imread(args.image)
        if frame is None:
            print("Failed to load image.")
            return
    else:
        print(f"Opening camera {args.camera}")
        cap = cv2.VideoCapture(args.camera)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            print("Failed to capture image from camera.")
            return

  
    # Enforce calibration resolutio
    
    current_height, current_width = frame.shape[:2]
    print(f"Runtime resolution: {current_width} x {current_height}")
    if current_width != calib_width or current_height != calib_height:
        print("Resizing frame to match calibration resolution...")
        frame = cv2.resize(frame, (calib_width, calib_height))

    
    # Detect objects
   
    detector = Detector()
    detected_objects = detector.find_objects(
        frame,
        color_name=args.color,
        shape_type=args.shape,
        show_overlay=True
    )

    if not detected_objects:
        print("No matching objects found.")
        return

    print(f"Detected {len(detected_objects)} matching objects.")

    
    # Build list of all objects within workspace
    
    robot_targets = []
    for obj in detected_objects:
        u, v = obj["pixel_center"]
        robot_x, robot_y = pixel_to_robot(u, v, H)
        print(f"Pixel ({u}, {v}) -> Robot ({robot_x:.2f}, {robot_y:.2f})")

        if is_within_workspace(robot_x, robot_y):
            robot_targets.append({
                "pixel_center": (u, v),
                "robot_coords": (robot_x, robot_y),
                "Shape": obj["Shape"],
                "color": obj["color"]
            })

    if not robot_targets:
        print("No objects are within robot workspace.")
        print(f"Workspace X: [{WORKSPACE_X_MIN}, {WORKSPACE_X_MAX}] | Y: [{WORKSPACE_Y_MIN}, {WORKSPACE_Y_MAX}]")
        return

    
    # Pick all objects sequentially
    
    for target in robot_targets:
        u, v = target["pixel_center"]
        robot_x, robot_y = target["robot_coords"]
        shape_type = target["Shape"]
        color = target["color"]

        print(f"\n Selected {color} {shape_type} at pixel ({u}, {v}) → Robot ({robot_x:.2f}, {robot_y:.2f})")

        if args.mode == "execute":
            print(f"Picking {color} {shape_type} at Robot ({robot_x:.2f}, {robot_y:.2f})...")
            execute_pick_and_place([{"robot_coords": (robot_x, robot_y)}])
        else:
            print("Plan mode: Robot motion not executed.")

if __name__ == "__main__":
    main()