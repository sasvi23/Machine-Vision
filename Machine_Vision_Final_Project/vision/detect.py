import cv2
import numpy as np


class Detector:
    def __init__(self):
        # HSV color ranges
        self.colors = {
        "red": [
        ([0, 150, 50], [10, 255, 255]),      
        ([160, 100, 100], [180, 255, 255])    
    ],
    "green": [
        ([35, 50, 10], [85, 255, 255])
    ],
    "blue": [
        ([90, 100, 50], [140, 255, 255])
    ],
    "yellow": [
        ([20, 100, 100], [35, 255, 255])
    ]
}

    def find_objects(self, image, color_name="any", shape_type="any", show_overlay=False):
        output = image.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        detected_objects = []

        
        if color_name != "any" and color_name in self.colors:
            masks = []
            for lower, upper in self.colors[color_name]:
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                masks.append(mask)

            mask = masks[0]
            for i in range(1, len(masks)):
                mask = cv2.bitwise_or(mask, masks[i])

            colors_to_process = [color_name]

        # If any color → process all
        elif color_name == "any":
            colors_to_process = self.colors.keys()
        else:
            print("Unsupported color")
            return []

        for color in colors_to_process:

            if color_name == "any":
                masks = []
                for lower, upper in self.colors[color]:
                    m = cv2.inRange(hsv, np.array(lower), np.array(upper))
                    masks.append(m)

                mask = masks[0]
                for i in range(1, len(masks)):
                    mask = cv2.bitwise_or(mask, masks[i])

            # Morphological cleanup
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < 800:
                    continue

                perimeter = cv2.arcLength(cnt, True)
                if perimeter == 0:
                    continue

                circularity = (4 * np.pi * area) / (perimeter ** 2)

                if circularity > 0.8:
                    detected_shape = "circle"
                else:
                    detected_shape = "square"

                if shape_type != "any" and detected_shape != shape_type:
                    continue

                M = cv2.moments(cnt)
                if M["m00"] == 0:
                    continue

                u = int(M["m10"] / M["m00"])
                v = int(M["m01"] / M["m00"])

                detected_objects.append({
                    "pixel_center": (u, v),
                    "Shape": detected_shape,
                    "color": color
                })

                if show_overlay:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.circle(output, (u, v), 5, (0, 0, 255), -1)
                    cv2.putText(
                        output,
                        f"{color} {detected_shape}",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

        if show_overlay:
            cv2.imshow("Detection", output)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return detected_objects