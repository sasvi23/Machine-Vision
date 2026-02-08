import cv2
import matplotlib.pyplot as plt

img = cv2.imread("images/capture_img1.png.jpg")


if img is None:
    print("Image not found. Check the path!")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray, cmap='gray')
    plt.show()
