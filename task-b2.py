import cv2
from datetime import date

# 1. Opening the snapshot image 
img = cv2.imread('images/robodk_snapshot.png')

if img is None:
    print("Error: Could not find images/robodk_snapshot.png")
else:
    # 2. Printing image shape information (height x width, channels) 
    h, w, c = img.shape
    print(f"Image Shape: {h} x {w}, Channels: {c}")

    # 3. Annotating two parts with shapes and names 
    
    # Object 1: Yellow Cube (Cube 1)
    
    cv2.rectangle(img, (70, 345), (180, 435), (255, 0, 0), 2) # Blue rectangle
    cv2.putText(img, 'Cube 1', (70, 335), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Object 2: Pink Cylinder (Cylinder 1)
    
    cv2.circle(img, (510, 110), 95, (0, 0, 255), 2) # Red circle
    cv2.putText(img, 'Cylinder 1', (430, 230), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 4. Name and date at the top
    today = date.today().strftime("%Y-%m-%d")
    header_text = f"Sasvi {today}"
    cv2.putText(img, header_text, (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

    # 5. Showing and saving the result 
    cv2.imshow('Task B2 - Final Annotated Snapshot', img)
    cv2.imwrite('images/task-b2-result.png', img)
    print("Annotated image saved as task-b2-result.png")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()