import cv2
import numpy as np
import json
import datetime

# -------------------------------
# Global lists for points
# -------------------------------
image_points = []
robot_points = []

# -------------------------------
# Mouse click callback
# -------------------------------
def click_event(event, x, y, flags, param):
    """
    Record pixel points when the user clicks on the calibration image.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        img, img_window = param
        image_points.append([x, y])
        cv2.circle(img, (x, y), 6, (0, 0, 255), -1)
        cv2.imshow(img_window, img)
        print(f"Pixel point selected: ({x}, {y})")

# -------------------------------
# Main calibration function
# -------------------------------
def run_calibration(image_path="image.jpg"):
    """
    Load saved image, select pixel points,
    input robot coordinates, compute homography, and save to JSON.
    """
    # -------------------------------
    # Load image
    # -------------------------------
    print(f"Loading image from {image_path}...")
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image.")
        return

    img_window = "Calibration"
    img_copy = img.copy()

    # -------------------------------
    # Collect pixel points
    # -------------------------------
    print("\nClick at least 4 pixel points on the image (clockwise recommended).")
    print("Press ESC when done selecting points.")

    cv2.imshow(img_window, img_copy)
    cv2.setMouseCallback(img_window, click_event, param=(img_copy, img_window))

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break

    cv2.destroyAllWindows()

    if len(image_points) < 4:
        print("Need at least 4 points for homography.")
        return

    # -------------------------------
    # Collect robot points
    # -------------------------------
    print("\nEnter corresponding robot X,Y coordinates (mm) for each pixel point:")
    for i in range(len(image_points)):
        while True:
            try:
                X = float(input(f"Robot X for point {i+1}: "))
                Y = float(input(f"Robot Y for point {i+1}: "))
                robot_points.append([X, Y])
                break
            except ValueError:
                print("⚠ Please enter valid numeric values.")

    # -------------------------------
    # Compute homography
    # -------------------------------
    H, _ = cv2.findHomography(
        np.array(image_points, dtype=np.float32),
        np.array(robot_points, dtype=np.float32)
    )

    # -------------------------------
    # Save calibration
    # -------------------------------
    data = {
        "H": H.tolist(),
        "image_width": img.shape[1],
        "image_height": img.shape[0],
        "date": str(datetime.datetime.now()),
        "camera_id": None,
        "notes": f"Calibration from saved image with {len(image_points)} points"
    }

    with open("calibration.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\n✅ Calibration saved successfully as 'calibration.json'.")
    print("Homography matrix H:")
    print(H)

# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    run_calibration("IMAGE.jpg")