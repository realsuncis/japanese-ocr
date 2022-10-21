import cv2
import numpy as np
import imutils
from PIL import Image

class CV2Processes:

    # get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(image):
        return cv2.medianBlur(image, 5)

    # thresholding
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # dilation
    def dilate(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    # erosion
    def erode(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    # opening - erosion followed by dilation
    def opening(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # canny edge detection
    def canny(image):
        return cv2.Canny(image, 100, 200)

    def processImage(img):
        image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = CV2Processes.get_grayscale(image)
        opening = CV2Processes.opening(gray)
        return Image.fromarray(opening)

    @staticmethod
    def is_contour_bad(c, imgW, imgH):
        x, y, w, h = cv2.boundingRect(c)

        xMin = 0;
        yMin = 0;
        xMax = imgW - 1
        yMax = imgH - 1

        if (x <= xMin or y <= yMin or w >= xMax or h >= yMax):
            return True
        else:
            return False

    @staticmethod
    def removeShitAroundBorder(img):
        # load the shapes image, convert it to grayscale, and edge edges in
        # the image
        image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        #image = np.pad(imageTemp.copy(), ((1, 1), (1, 1), (0, 0)), 'edge')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        #cv2.imshow("Original", image)
        # find contours in the image and initialize the mask that will be
        # used to remove the bad contours
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)
        mask = np.ones(image.shape[:2], dtype="uint8") * 255
        # loop over the contours
        for c in cnts:
            # if the contour is bad, draw it on the mask
            if CV2Processes.is_contour_bad(c, img.size[0], img.size[1]):
                hull = cv2.convexHull(c, False)
                cv2.drawContours(image, [hull], -1, color=(255,255,255), thickness=cv2.FILLED)
                #cv2.fillPoly(mask, [c], color=(0,0,0))
        # remove the contours from the image and show the resulting images
        #image = cv2.bitwise_and(image, image, mask=mask)
        #imageTemp = image[1:-1,1:-1,:]
        #cv2.imshow("Mask", mask)
        #cv2.imshow("After", image)
        return Image.fromarray(image)