try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import numpy as np
import cv2

cFilename = "test.png"
wImage = cv2.imread(cFilename)
hsv = cv2.cvtColor(wImage, cv2.COLOR_RGB2HSV)
lower_yellow = np.array([52,120,120])
upper_yellow = np.array([100,255,255])
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
combinedImages = cv2.bitwise_and(wImage, wImage, mask=mask)
#wGrayImage = cv2.cvtColor(wImage, cv2.COLOR_BGR2GRAY)
#garbage, wBlackWhiteImage = cv2.threshold(wGrayImage, 160, 255, cv2.THRESH_BINARY)
#wTestTh = cv2.adaptiveThreshold(wGrayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
#                                cv2.THRESH_BINARY, 11, 5)
#wTestInverted = cv2.bitwise_not(wTestTh)
wText = pytesseract.image_to_string(mask)
print(wText)
cv2.imshow("image", wImage)
cv2.imshow("mask", mask)
cv2.imshow("combined", combinedImages)
cv2.waitKey(0)
cv2.destroyAllWindows()