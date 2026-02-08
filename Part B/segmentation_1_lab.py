import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


os.makedirs("Results", exist_ok=True)

images = [
    "images/capture_img1.jpg",
    "images/capture_img2.jpg",
    "images/capture_img3.jpg",
    "images/capture_img4.jpg"
]

MIN_AREA = 400

for path in images:
    print(f"\nProcessing: {path}")

    img = cv2.imread(path)
    if img is None:
        print(f"Error: Could not load {path}")
        continue

    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    cv2.imwrite(f"results/gray_{os.path.basename(path)}", gray)

    
    plt.figure()
    plt.hist(gray.ravel(), 256)
    plt.title("Histogram")
    plt.savefig(f"results/hist_{os.path.basename(path)}")
    plt.close()

    
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

    
    _, bin_img = cv2.threshold(
        gray_blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    
    white_pixels = np.sum(bin_img == 255)
    black_pixels = np.sum(bin_img == 0)
    if black_pixels > white_pixels:
        bin_img = cv2.bitwise_not(bin_img)

    
    cv2.imwrite(f"results/bin_{os.path.basename(path)}", bin_img)

    
    kernel = np.ones((3, 3), np.uint8)
    clean = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, iterations=2)
    clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel, iterations=2)

    
    cv2.imwrite(f"results/morph_{os.path.basename(path)}", clean)

    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(clean)

    print(f"Detected {num_labels - 1} raw components")

    
    annotated = img.copy()

    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        cx, cy = centroids[i]

        
        if area < MIN_AREA:
            continue

        
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)

        
        cv2.circle(annotated, (int(cx), int(cy)), 5, (0, 0, 255), -1)

        
        cv2.putText(
            annotated, f"ID {i}", (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2
        )

    
    cv2.imwrite(f"results/annotated_{os.path.basename(path)}", annotated)

    print(f"Saved annotated image: results/annotated_{os.path.basename(path)}")

print("\nProcessing complete!")
