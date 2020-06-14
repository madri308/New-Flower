import cv2

class ImageReader:
    RGB_images = [None,None,None]
    def __init__(self, paths):
        for i in range(3):
            if paths[i] != '':
                self.RGB_images[i] =  cv2.cvtColor(cv2.imread(paths[i]), cv2.COLOR_BGR2RGB)
    def getResults(self):
        return self.RGB_images
