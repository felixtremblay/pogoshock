try:
    from PIL import Image, ImageGrab
except ImportError:
    import Image, ImageGrab
import pytesseract
import numpy as np
import cv2
import re
import os
import time

bbox = [0, 0, 1000, 1000]
progressThreshold = -6 
delay = 4

def setup():
    # Select the region of interest
    #image = np.array(ImageGrab.grab(bbox=(0, 0, 1000, 1000)))
    #global boundingBox
    #boundingBox = cv2.selectROI(image, False)
    #print(boundingBox)
    pass

def mainLoop():
    global progressThreshold
    global delay
    print("\nStarting the main loop...\n")
    startTime = time.time()
    lastProgress = 0.0
    while True:
        time.sleep(delay)
        currentProgress = getProgress()
        print("\nCurrent Progress : " + str(currentProgress))
        if currentProgress != None:
            progressDiff = currentProgress - lastProgress
            print("Last Progress : " + str(lastProgress))
            print('Progress diff : ' + str(progressDiff))
            if progressDiff <= progressThreshold:
                os.system("say noob")
            lastProgress = currentProgress
        endTime = time.time()
        loopTime = endTime - startTime
        print("Loop execution time : " + str(loopTime) + "\n")
        startTime = endTime


def getProgress():
    # Get the image
    image = np.array(ImageGrab.grab(bbox=bbox))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([52,120,120])
    upper_yellow = np.array([100,255,255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    invertedMask = cv2.bitwise_not(mask)
    cv2.imshow("mask", invertedMask)
    cv2.waitKey(0)

    # Get the text
    text = pytesseract.image_to_string(invertedMask)

    # Find the value
    progressFinder = re.search(r'FTcuber\s[^d]\s\d+\.\d', text)
    progress = None
    if progressFinder:
        progress = float(re.search(r'\d+\.\d', progressFinder.group()).group())

    return progress


if __name__ == "__main__":
    setup()
    mainLoop()
    cv2.destroyAllWindows()