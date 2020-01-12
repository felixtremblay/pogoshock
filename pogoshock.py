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
#import webbrowser
import serial

bbox = [0, 0, 800, 800]
progressThreshold = -1 # In percentage
refreshRate = 5 # In seconds
shockTime = 1000
serialConnection = None

def setup():
    global serialConnection
    print("\nInitializing the serial connection...")
    serialConnection = serial.Serial('/dev/tty.wchusbserial14120', 9600)
    time.sleep(3)
    print("Serial connection established with {}".format(serialConnection.name))

def mainLoop():
    global progressThreshold
    global refreshRate
    print("\nStarting the main loop...\n")
    lastProgress = 0.0
    while True:
        startTime = time.time()
        currentProgress = getProgress()
        if currentProgress != None:
            progressDiff = currentProgress - lastProgress
            print("Current Progress : {:.2f}".format(currentProgress))
            print("Last Progress : {:.2f}".format(lastProgress))
            print("Progress diff : {:.2f}".format(progressDiff))
            if progressDiff <= progressThreshold:
                punishThePlayer()
            lastProgress = currentProgress

            endTime = time.time()
            loopTime = endTime - startTime
            extraTime = refreshRate - loopTime
            if extraTime > 0.0:
                print("Loop time : {:.2f}\n".format(refreshRate))
                time.sleep(extraTime)
            else:
                print("Warning: Loop time exceeded refresh rate")
                print("Loop time : {:.2f}\n".format(loopTime))
        else:
            print("Couldn't recognize the current progress\n")


def getProgress():
    # Get the image
    image = np.array(ImageGrab.grab(bbox=bbox))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([52,120,120])
    upper_yellow = np.array([100,255,255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    invertedMask = cv2.bitwise_not(mask)
    #cv2.imshow("mask", invertedMask)
    #cv2.waitKey(0)

    # Get the text
    text = pytesseract.image_to_string(invertedMask)

    # Find the value
    progressFinder = re.search(r'FTcuber\s[^d]\s\d+\.\d', text)
    progress = None
    if progressFinder:
        progress = float(re.search(r'\d+\.\d', progressFinder.group()).group())

    return progress


def punishThePlayer():
    #address = "https://youtu.be/ZQ7oqmikZDQ?t=47"
    #webbrowser.open(address, new=1)
    serialConnection.write("{}\n".format(shockTime).encode('utf-8'))

if __name__ == "__main__":
    setup()
    mainLoop()
    cv2.destroyAllWindows()