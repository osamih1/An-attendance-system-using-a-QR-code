# tessing the detection of the QR code on a set of images
import os
import cv2
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode
import numpy as np

data_dir = "data"

for j in os.listdir(data_dir):
    img = cv2.imread(os.path.join(data_dir,j))

    info_qrs = decode(img)
    for info_qr in info_qrs:
        data = info_qr.data
        rect = info_qr.rect
        polygon = info_qr.polygon

        img = cv2.rectangle(img, (rect.left, rect.top), (rect.left+rect.width, rect.top+rect.height), (0,255,0), 5)
        img = cv2.polylines(img, [np.array(polygon)], True, (0,0,255), 5)


    plt.imshow(img)
    plt.show()