# Machine Vision - Lab Assignment: Segmentation

### Team Members
- Udalmaththa Gamage Chathuri Anuththara Karunarathna, Anu2344, amk1004058@student.hamk.fi
- Sasvi Vidunadi Ranasinghe, sasvi23, amk1005778@student.hamk.fi
- Himihami Mudiyanselage Lahiru Bandaranayake, LahiruBandaranayake, amk1004101@student.hamk.fi
- Pramoda Medis, PramoGIT, amk1003750@student.hamk.fi

## Summary
This repository contains the image segmentation tasks using **OpenCV** and **Python** for the Machine Vision course (IR00EU71-3001) at Häme University of Applied Sciences. The project implements a complete pipeline for detecting and annotating objects in both simulated (RoboDK) and real-world images.

---

## 2026-02-08

**Lab Assignment by:**
- Udalmaththa Gamage Chathuri Anuththara Karunarathna
- Sasvi Vidunadi Ranasinghe
- Himihami Mudiyanselage Lahiru Bandaranayake
- Pramoda Medis

### Image Segmentation and Object Detection

We have completed the image segmentation tasks using Python and OpenCV according to the lab handout instructions.

- Set up Python environment and installed necessary libraries via `pip`.

- Created `segmentation_1_lab.py` to process both simulated and real images with a unified pipeline that works for all images.

- **Part B - Real Images (completed during lab session):**
    - Captured 4 real images as required:

        - Image 1: Black paper markers (6 shapes: 4 squares with notches + 2 circles)

        - Image 2: Mosaic tiles all same dark color (4 dark green/teal tiles)

        - Image 3: Mosaic tiles with mixed dark colors (4 dark green + 2 yellow tiles)

        - Image 4: Mosaic tiles with mixed bright and dark colors (12 tiles: green, yellow, blue)

    - Implemented complete segmentation pipeline:

        - Grayscale conversion using `cv2.cvtColor`
        - Histogram analysis using `matplotlib`

        - Gaussian blur (5×5 kernel) for noise reduction

        - Otsu's automatic thresholding

        - Binary normalization to ensure objects are white

        - Morphological opening and closing (3×3 kernel, 2 iterations each)

        - Connected component analysis using `cv2.connectedComponentsWithStats`

        - Area-based filtering (MIN_AREA = 400 pixels)

    - Annotated all detected objects with:
        - Green bounding rectangles using `cv2.rectangle`

        - Red centroids using `cv2.circle`

        - Blue ID labels using `cv2.putText`


- **Part A - Simulated Image (RoboDK) (completed after lab via group call):**
    - Created scenario in RoboDK with objects on white sheet of paper

    - Captured snapshot from simulated camera

    - Applied the same unified pipeline from Part B

    - Verified bimodal histogram distribution

- Generated step-by-step processing images for all inputs: grayscale, histogram, binary, morphological, and final annotated.

### Findings

**Ease/Difficulty** 
- Part B (real images) was completed during the lab session and was relatively straightforward once we understood the pipeline. 
- The main challenge was tuning MIN_AREA to filter noise while keeping real objects - we tested values of 300, 400, and 500 before settling on 400. 
- Part A (RoboDK simulation) was more difficult than expected due to a RoboDK license issue that required us to completely uninstall and reinstall the software during our group call. 
- Once RoboDK was working, creating the scenario and capturing the image was simple.


**Time/Speed** 
- Part B took approximately 3-4 hours during the lab session (image capture: 30 minutes, coding and testing: 2.5-3 hours, documentation: 30 minutes). 
- Part A was completed in a separate group call via screen sharing and took about 2 hours including troubleshooting the RoboDK license problem. 
- Once configured, each image processes in less than a second.

**Issues** 
- The biggest technical issue was RoboDK's license error which prevented us from capturing the simulated image initially. 
- We had to uninstall and reinstall RoboDK to fix it. For the segmentation itself, the main challenge was finding MIN_AREA that worked for all images - glossy tile reflections in Image 4 created bright spots, and table texture appeared as noise requiring morphological cleanup.



## Results

### Part B: Real Image Processing

We captured 4 real images during the lab session as specified in the assignment: black paper markers, tiles of same dark color, mixed dark colors, and mixed bright and dark colors. The pipeline processes each image through grayscale conversion, histogram analysis, Gaussian blur, Otsu's thresholding, morphological operations, and connected component analysis with area filtering.

### Image 1: Black Paper Markers
6 black paper shapes (4 squares with notches + 2 circles) on white background.

**Original Image:**

<img src="Part B/images/capture_img1.jpg" width="800"><br />

**Processing Pipeline:**

| Grayscale | Histogram |
|-----------|-----------|
| <img src="Part B/Results/gray_capture_img1.jpg" width="400"> | <img src="Part B/Results/hist_capture_img1.jpg" width="400"> |

| Binary (Otsu) | Morphological |
|---------------|---------------|
| <img src="Part B/Results/bin_capture_img1.jpg" width="400"> | <img src="Part B/Results/morph_capture_img1.jpg" width="400"> |

**Final Annotated Result:**

<img src="Part B/Results/annotated_capture_img1.jpg" width="800"><br />

---

### Image 2: Same Dark Color Tiles
4 dark green/teal glossy tiles - uniform color testing.

**Original Image:**

<img src="Part B/images/capture_img2.jpg" width="800"><br />

**Processing Pipeline:**

| Grayscale | Histogram |
|-----------|-----------|
| <img src="Part B/Results/gray_capture_img2.jpg" width="400"> | <img src="Part B/Results/hist_capture_img2.jpg" width="400"> |

| Binary (Otsu) | Morphological |
|---------------|---------------|
| <img src="Part B/Results/bin_capture_img2.jpg" width="400"> | <img src="Part B/Results/morph_capture_img2.jpg" width="400"> |

**Final Annotated Result:**

<img src="Part B/Results/annotated_capture_img2.jpg" width="800"><br />

---

### Image 3: Mixed Dark Colors
6 tiles with mixed colors: 4 dark green + 2 yellow.

**Original Image:**

<img src="Part B/images/capture_img3.jpg" width="800"><br />

**Processing Pipeline:**

| Grayscale | Histogram |
|-----------|-----------|
| <img src="Part B/Results/gray_capture_img3.jpg" width="400"> | <img src="Part B/Results/hist_capture_img3.jpg" width="400"> |

| Binary (Otsu) | Morphological |
|---------------|---------------|
| <img src="Part B/Results/bin_capture_img3.jpg" width="400"> | <img src="Part B/Results/morph_capture_img3.jpg" width="400"> |

**Final Annotated Result:**

<img src="Part B/Results/annotated_capture_img3.jpg" width="800"><br />

---

### Image 4: Mixed Bright and Dark Colors
12 tiles with highly varied colors: dark green, yellow, and bright blue with strong reflections.

**Original Image:**

<img src="Part B/images/capture_img4.jpg" width="800"><br />

**Processing Pipeline:**

| Grayscale | Histogram |
|-----------|-----------|
| <img src="Part B/Results/gray_capture_img4.jpg" width="400"> | <img src="Part B/Results/hist_capture_img4.jpg" width="400"> |

| Binary (Otsu) | Morphological |
|---------------|---------------|
| <img src="Part B/Results/bin_capture_img4.jpg" width="400"> | <img src="Part B/Results/morph_capture_img4.jpg" width="400"> |

**Final Annotated Result:**

<img src="Part B/Results/annotated_capture_img4.jpg" width="800"><br />

---

### Part A: Simulated Image (RoboDK)

We created a scenario in RoboDK with various shapes placed on a white sheet of paper to avoid detecting table holes. After resolving RoboDK license issues, the simulated camera captured a clean image with excellent contrast.

**Processing Pipeline:**

| Grayscale | Histogram |
|-----------|-----------|
| <img src="Part A/outputs/A2_gray.png" width="400"> | <img src="Part A/outputs/A2_histogram.png" width="400"> |

| Binary (Otsu) |
|---------------|
| <img src="Part A/outputs/A3_binary.png" width="400"> |

**Final Annotated Result:**

<img src="Part A/robodk_img1.png" width="800"><br />

---

## Discussion

### Q1: Which thresholding method gave the most stable results across your images?

We experimented with manual global thresholding, Otsu's method, and adaptive thresholding.

**Manual global thresholding** required different threshold values for each image. Image 1 needed around 100, while Image 4 needed approximately 130. This made it unsuitable for a unified pipeline.

**Adaptive thresholding** worked well for varying lighting but was noticeably slower and created artifacts from table texture. We tested block sizes from 11 to 51, but the extra morphological filtering needed made it impractical.

**Otsu's automatic thresholding** gave the best results for our unified code. It calculated different thresholds automatically: Image 1 got ~110, Image 2 ~95, Image 3 ~105, and Image 4 ~115. Combined with Gaussian blur, it handled all our images consistently.

However, Otsu struggled with Image 4 because the blue, yellow, and green tiles created three peaks in the histogram instead of two, making the single threshold suboptimal for all tile colors.

---

### Q2: Did preprocessing (filtering and/or contrast enhancement) and morphology help improve segmentation?

Yes, both were essential for real images.

**Gaussian Blur:**
We added a 5×5 Gaussian blur before thresholding. Without it, Image 2 had about 20-25 false detections from table texture. With blur, this dropped to 2-3. We tested 3×3, 5×5, 7×7, and 9×9 kernels - the 5×5 gave the best balance between noise reduction and edge preservation.

We didn't use contrast enhancement (CLAHE) because our lighting was decent, and when we tested it on Image 3, it actually amplified table texture noise.

**Morphological Operations:**
We used opening (erosion then dilation) and closing (dilation then erosion), both with 3×3 kernel and 2 iterations.

Image 2 went from ~25 components before morphology to ~8 after opening, then down to 4 tiles after closing and area filtering. Without morphology, we would need MIN_AREA above 800 to filter noise, which would eliminate small legitimate objects.

We tested 1-4 iterations - 1 was too weak, 3-4 started shrinking real objects too much. 2 iterations was the sweet spot.

---

### Q3: What kinds of errors still remain (false positives, missed objects, shape distortions)?

**False Positives:**
- Glossy blue tiles in Image 4 created bright reflections larger than 400 pixels that passed our area filter

- Image 3 has a sticker on one tile creating an internal bright spot - morphology connected it to the tile, but with different parameters it could be detected separately

- Occasionally shadows between close tiles were detected as thin separate objects

**Missed Objects:**
- We didn't capture white tiles, but they would be missed due to low contrast with white background (assignment mentions this is acceptable)

- In Image 4, we might have missed 1-2 tiles due to the tri-modal histogram affecting threshold selection

- Any object smaller than 400 pixels is intentionally filtered out

**Shape Distortions:**
- Circular markers in Image 1 get square bounding boxes

- No orientation information - rotated squares look identical to aligned squares

- Bounding boxes are axis-aligned, so tilted objects get oversized boxes

**Size Distortions:**
- Shadows are included in segmentation, making boxes 10-20% larger than actual tiles

- Holes/notches in Image 1 squares are filled in by thresholding, increasing detected area

**Merged Detections:**
- When tiles touch or are very close, morphological closing connects them into one blob (happened once in Image 3)

- No orientation detection as mentioned in assignment instructions

---

### Q4: How would you change the lighting or camera setup in the real lab to make segmentation easier?

**Lighting:**

1. **Diffused overhead lighting:** Use a softbox LED panel 60-80cm above the table at a slight angle to eliminate harsh reflections on glossy tiles. This would solve most of the reflection problems in Image 4.

2. **Avoid window light:** Our setup had some ambient window light creating uneven illumination. A controlled environment with only artificial lighting would help.

3. **Polarizing filters:** For glossy tiles, crossed polarizers on camera and light source (90° to each other) would eliminate specular reflections while keeping diffuse reflection.

**Camera:**

1. **Higher resolution:** Moving from current resolution to 1920×1080 would give 4-5x more pixels, allowing us to detect smaller objects with lower MIN_AREA while still filtering noise.

2. **Perpendicular mounting:** Mount camera directly above table with a stable stand to eliminate perspective distortion.

3. **Fixed settings:** Lock focus and exposure instead of auto mode for consistent captures.

**Background:**

1. **Contrasting matte background:** Use dark blue or green matte sheet instead of white paper. This would give good contrast for both light and dark tiles and create clear bimodal histograms.

2. **Non-glossy surface:** The white paper has slight texture and glossiness. A completely matte surface would eliminate texture noise in binary images.

With diffused lighting alone, we estimate we could eliminate 70-80% of our reflection issues and reduce MIN_AREA to 200-250 pixels for better small object detection.

---

### Process Reflection

**Team Organization:**
We completed Part B during the lab session working together. For Part A, we had a group call where one person shared their screen while working with RoboDK, and others helped troubleshoot and test the code.

**How Easy/Difficult:**
Part B was straightforward once we understood the pipeline. The hardest part was deciding on MIN_AREA - too low kept noise, too high removed small real objects. We settled on 400 after testing.

Part A was unexpectedly difficult because of RoboDK license issues. The software kept showing a license error when we tried to capture the snapshot. We spent about 45 minutes troubleshooting before deciding to completely uninstall and reinstall RoboDK, which fixed the problem. After that, setting up the scenario and capturing the image was easy.

**Time Investment:**
- Part B (lab session): 3-4 hours total
  - Image capture: 30 minutes  
  - Pipeline coding: 2 hours
  - Parameter testing: 1 hour
  - Documentation: 30 minutes
- Part A (group call): 2 hours
  - RoboDK troubleshooting: 45 minutes
  - Scenario setup: 30 minutes
  - Code testing: 45 minutes

**Processing Speed:**
Each image processes in under 1 second, fast enough for real-time applications.

**Key Learnings:**

The biggest lesson was that real images need much more processing than simulated ones. The RoboDK image worked perfectly with just Otsu's threshold, but real images needed blur, morphology, and area filtering.

We also learned that histogram shape really matters - Image 4's three-peak histogram made Otsu's threshold work poorly, which we only understood after looking at the histogram visualization.

**What Worked Well:**
`connectedComponentsWithStats` gave us area, centroid, and bounding box in one call, making area filtering simple. Saving intermediate images (gray, binary, morph) was very helpful for debugging.

**Unexpected Issues:**
The RoboDK license problem was completely unexpected and cost us significant time. We also didn't anticipate how much the glossy tile reflections would interfere with segmentation.

---

## Technical Documentation

### Complete Code

```python
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
    
    # Grayscale conversion
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"Results/gray_{os.path.basename(path)}", gray)
    
    # Histogram
    plt.figure()
    plt.hist(gray.ravel(), 256)
    plt.title("Histogram")
    plt.savefig(f"Results/hist_{os.path.basename(path)}")
    plt.close()
    
    # Gaussian blur
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Otsu's thresholding
    _, bin_img = cv2.threshold(
        gray_blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    
    # Normalize binary orientation
    white_pixels = np.sum(bin_img == 255)
    black_pixels = np.sum(bin_img == 0)
    if black_pixels > white_pixels:
        bin_img = cv2.bitwise_not(bin_img)
    
    cv2.imwrite(f"Results/bin_{os.path.basename(path)}", bin_img)
    
    # Morphological operations
    kernel = np.ones((3, 3), np.uint8)
    clean = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, iterations=2)
    clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    cv2.imwrite(f"Results/morph_{os.path.basename(path)}", clean)
    
    # Connected component analysis
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(clean)
    
    print(f"Detected {num_labels - 1} raw components")
    
    # Annotation with area filtering
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
    
    cv2.imwrite(f"Results/annotated_{os.path.basename(path)}", annotated)
    
    print(f"Saved annotated image: Results/annotated_{os.path.basename(path)}")

print("\nProcessing complete!")
```

---


