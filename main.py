import pytesseract
import pyscreenshot as screenshot
import configparser
from position import Position
import win32api, win32gui
import threading
import time
import pyperclip
from window import Window
from mouse import MouseManager
from PIL import Image
from PIL import ImageEnhance
from cv2_processes import CV2Processes

def resizeImage(img, ratio):
    width = (int)(img.size[0]*ratio)
    height = (int)(img.size[1]*ratio)
    return img.resize((width,height), Image.ANTIALIAS)

def sortCoordinates(item1, item2):
    if item1 > item2:
        return (item2, item1)
    else:
        return (item1, item2)


def highPassFilter(im):
    threshold = 60
    im = im.point(lambda p: p > threshold and 255)
    return im


def main(winWindow):
    last_state_click = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    mouseMngr = MouseManager()
    firstPos = Position(0, 0)
    captureArea = False
    while True:
        redrawRect = False
        try:
            mousePos = mouseMngr.getPosition()
        except:
            time.sleep(0.005)
            continue

        if mouseMngr.positionChanged():
            redrawRect = True

        state_click = win32api.GetKeyState(0x01) #Left mouse button
        state_shift = win32api.GetKeyState(0x10) #Shift key
        if state_click != last_state_click:  #Left click Button state changed
            last_state_click = state_click
            if state_click < 0: #Left button Pressed
                if state_shift < 0: #Shift button pressed
                    firstPos.x = mousePos.x
                    firstPos.y = mousePos.y
                    captureArea = True
            else: #Left button released
                if captureArea:
                    captureArea = False
                    if firstPos.x != mousePos.x and firstPos.y != mousePos.y:
                        x1, x2 = sortCoordinates(firstPos.x, mousePos.x)
                        y1, y2 = sortCoordinates(firstPos.y, mousePos.y)
                        winWindow.setRectangle(0, 0, 0, 0)
                        winWindow.InvalidateRect()
                        print('capture')
                        im = screenshot.grab(bbox=(x1, y1, x2, y2))
                        im.show()
                        im = resizeImage(im, 8)
                        im.show()
                        enhancer = ImageEnhance.Sharpness(im)
                        #im = enhancer.enhance(4.0)
                        #im.show()
                        im = highPassFilter(im)
                        im.show()
                        im = CV2Processes.removeShitAroundBorder(im)
                        #im = CV2Processes.processImage(im)
                        im.show()
                        text = pytesseract.image_to_string(im, lang="jpn_vert")
                        text = text.replace(" ", "")
                        text = text.replace("\n", "")
                        pyperclip.copy(text)
                        print(text)
        if captureArea and redrawRect:
            winWindow.setRectangle(firstPos.x, firstPos.y, mousePos.x, mousePos.y)
            winWindow.InvalidateRect()

        mouseMngr.update()
        time.sleep(0.005)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    tesseractPath = config['TESSERACT']['TesseractPath']
    if not tesseractPath:
        print('No Tesseract file path specified')
        exit(-1)
    pytesseract.pytesseract.tesseract_cmd = tesseractPath
    try:
        version = pytesseract.pytesseract.get_tesseract_version()
        print('Loaded Tesseract version', version)
    except:
        print('Tesseract not found')
        exit(-1)
    winWindow = Window()
    t = threading.Thread(target=main, args=[winWindow])
    t.start()
    win32gui.PumpMessages()

