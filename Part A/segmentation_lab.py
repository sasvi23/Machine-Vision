import os, cv2, numpy as np, matplotlib.pyplot as plt

IMG_DIR = "images"
OUT_DIR = os.path.join(IMG_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)
IMG_PATH = os.path.join(IMG_DIR, "robodk_img1.png")

bgr = cv2.imread(IMG_PATH)
if bgr is None: raise FileNotFoundError(IMG_PATH)
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
cv2.imwrite(os.path.join(OUT_DIR, "A2_gray.png"), gray)

plt.figure(figsize=(5,3))
plt.title("Grayscale histogram"); plt.xlabel("Intensity"); plt.ylabel("Pixel count")
plt.hist(gray.ravel(), bins=256, range=(0,256), color='steelblue')
plt.tight_layout(); plt.savefig(os.path.join(OUT_DIR, "A2_histogram.png"), dpi=150); plt.close()

# Otsu threshold
otsu_t, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Ensure objects are white (invert if needed)
if bin_img.mean() < 127: bin_img = cv2.bitwise_not(bin_img)
cv2.imwrite(os.path.join(OUT_DIR, "A3_binary.png"), bin_img)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_img, connectivity=4, ltype=cv2.CV_32S)
print(f"Found {num_labels-1} objects")
for i in range(1, num_labels):
    x,y,w,h,area = stats[i]; cx,cy = centroids[i]
    print(f"ID {i:02d}: area={area} bbox=({x},{y},{w},{h}) centroid=({cx:.1f},{cy:.1f})")

canvas = bgr.copy()
for i in range(1, num_labels):
    x,y,w,h,area = stats[i]; cx,cy = centroids[i]; cx_i, cy_i = int(round(cx)), int(round(cy))
    cv2.rectangle(canvas, (x,y), (x+w,y+h), (0,255,0), 2)
    cv2.circle(canvas, (cx_i,cy_i), 4, (0,0,255), -1)
    cv2.putText(canvas, f"ID {i} ({cx_i},{cy_i})", (x, max(0, y-6)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA)

cv2.imwrite(os.path.join(OUT_DIR, "A6_annotated.png"), canvas)
print("Saved outputs in images/outputs/")