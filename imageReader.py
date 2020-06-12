import cv2
import numpy as np
import matplotlib.pyplot as plt

class imageReader:
    pixels = []
    def __init__(self, url):
        self.url = url
        img = cv2.imread(self.url)
        self.RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.pixels = np.array(self.RGB_img)
    def showImage(self):
        cid = plt.figure().canvas.mpl_connect('button_press_event', self.onclick)
        plt.imshow(self.pixels)
        plt.show()
    def onclick(self,event):
        try:
            if event.ydata is not None or event.xdata is not None:
                y = int(event.ydata)
                x = int(event.xdata)
                print('color=%s, xPixel=%f, yPixel=%f' %
                    (self.RGB_img[y,x], x, y))
                print(self.pixels[2][2])
            else:
                raise ValueError("What's up with that?")
        except ValueError:
            print("Oops!  Estas afuera de la imagen. Intenta de nuevo...")