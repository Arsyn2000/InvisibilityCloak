import cv2
import numpy as np
import time

print(cv2.__version__)

# Recording a Video using Webcam
vid_capture = cv2.VideoCapture(0)
vid_cod = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter("Invisible2.mp4", vid_cod, 20.0, (640,480))

while(True):
     # Capture each frame of webcam video
     ret,frame = vid_capture.read()
     cv2.imshow("My cam video", frame)
     output.write(frame)
     # Close and break the loop after pressing "x" key
     if cv2.waitKey(1) &0XFF == ord('x'):
         break

# close the already opened camera
vid_capture.release()
# close the already opened file
output.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()

# ------------------------------------------------------------------------------------------------------------
# taking Invisible.mp4 as input.
capture_video = cv2.VideoCapture("Invisible.mp4")

# give the camera to warm up
# Python time sleep function is used to add delay in the execution of the program
time.sleep(1)
count = 0
background = 0

# capturing the background in range of 60
# you should have video that have some seconds
# dedicated to background frame so that it
# could easily save the background image
for i in range(60):
    return_val, background = capture_video.read()
    if return_val == False:
        continue
print(background)
print(return_val)
background = np.flip(background, axis=1)  # flipping of the frame

# we are reading from video
while (capture_video.isOpened()):
    return_val, img = capture_video.read()
    if not return_val:
        break
    count = count + 1
    img = np.flip(img, axis=1)

    # convert the image - BGR to HSV
    # as we focused on detection of red color

    # converting BGR to HSV for better
    # detection or you can convert it to gray
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # -------------------------------------BLOCK----------------------------#
    # ranges should be carefully chosen
    # setting the lower and upper range for mask1
    lower_red = np.array([100, 40, 40])
    upper_red = np.array([100, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    # setting the lower and upper range for mask2
    lower_red = np.array([155, 40, 40])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    # ----------------------------------------------------------------------#

    # the above block of code could be replaced with
    # some other code depending upon the color of your cloth
    mask1 = mask1 + mask2

    # Refining the mask corresponding to the detected red color
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3),
                                                            np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv2.bitwise_not(mask1)

    # Generating the final output
    res1 = cv2.bitwise_and(background, background, mask=mask1)
    res2 = cv2.bitwise_and(img, img, mask=mask2)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("INVISIBLE MAN", final_output)
    k = cv2.waitKey(10)
    if k == 27:
        break
