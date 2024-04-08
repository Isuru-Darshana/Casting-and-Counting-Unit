import cv2 as cv 
import os

cam = cv.VideoCapture(0)
cv.namedWindow("Python Webcam Screenshot App")
img_counter = 0

# Set your folder path here where you want to save images
folder_path = 'your_folder_path'

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("failed to grab frame")
        break
    cv.imshow("test", frame)

    k = cv.waitKey(1)
     
    if k%256 == 27:
        # ESC pressed 
        print("Escape hit, closing the app")
        break

    elif k%256 == 32:
        # SPACE pressed
        img_name = os.path.join(folder_path, f"opencv_frame_{img_counter}.png")
        cv.imwrite(img_name, frame)
        print(f"{img_name} written!")
        img_counter += 1

cam.release()
cv.destroyAllWindows()
