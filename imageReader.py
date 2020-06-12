import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

class imageReader:
    def __init__(self, url):
        self.url = url
    def getImage(self):
        img = cv2.imread(self.url)
        imgplot = plt.imshow(img)
        plt.show()

        with Image.open('path/to/file.jpg') as img:
        img.show()

reader1 = imageReader('C:/Users/emema/Documents/TEC/2020/SEM_I/Analisis/New-Flower/f1.jpg')
reader1.getImage()