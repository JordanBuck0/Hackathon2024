import os
import shutil
import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_red_dots(image_path, threshold=200):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for red color in HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv_image, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv_image, lower_red, upper_red)

    # Combine the masks
    red_mask = mask1 + mask2

    # Find contours in the mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area (to remove noise)
    red_dots = [cnt for cnt in contours if cv2.contourArea(cnt) > threshold]

    # Draw contours on the original image
    output_image = image.copy()
    cv2.drawContours(output_image, red_dots, -1, (0, 255, 0), 2)

    # Save the result (overwritten)
    cv2.imwrite(image_path, output_image)
   
    # Print the number of red dots detected
    print(f"Number of red dots detected: {len(red_dots)}")

if __name__ == "__main__":
    input_dir = 'SAR_Images'
    output_dir = 'SAR_Images_Processed'

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.jpg'):  # Adjust the file extension as needed
            source_img = os.path.join(input_dir, filename)
            destination_img = os.path.join(output_dir, filename[:-4] + '_processed.jpg')  # Modify the output filename
            shutil.copy2(source_img, destination_img) # copy the original images into the new folder
            detect_red_dots(destination_img) # detect red dots on destination images (overwriting them)

    print("Processing complete!")
