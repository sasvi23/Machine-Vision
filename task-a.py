import cv2
import matplotlib.pyplot as plt

# 1. Loading the image
img = cv2.imread('images/task-a-image.jpeg')

if img is None:
    print("Check your file path")
else:
    # 2. Spliting channels
    b, g, r = cv2.split(img)

    # 3. Creating the Grid 
    fig, axs = plt.subplots(1, 4, figsize=(15, 5))

    # 4. Converting for display
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 5. Showing results with titles
    axs[0].imshow(img_rgb)
    axs[0].set_title('Original - Sasvi') 
    
    # Showing grayscale channels
    axs[1].imshow(r, cmap='gray')
    axs[1].set_title('Red Channel')
    
    axs[2].imshow(g, cmap='gray')
    axs[2].set_title('Green Channel')
    
    axs[3].imshow(b, cmap='gray')
    axs[3].set_title('Blue Channel')

    # 6. Saving
    plt.savefig('images/task-a-result.png')
    plt.show()
