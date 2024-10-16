import cv2
import numpy as np
import matplotlib.pyplot as plt

"""Задание:
Загрузить изображение и отобразить его.
Применить несколько фильтров, таких как размытие (Gaussian Blur), сглаживание (Median Blur) и резкость (Sharpen).
Преобразовать цветное изображение в черно-белое и отобразить результат."""

# read image
src = cv2.imread('./Data/Vanya.jpg', cv2.IMREAD_UNCHANGED)

# Gaussian Smoothing
dst = cv2.GaussianBlur(src,(5,5),cv2.BORDER_DEFAULT)
# cv2.imshow("Gaussian Smoothing", dst)

# Median Blurring
median = cv2.medianBlur(src,5)
# cv2.imshow("Median Blurring", median)

# Sharpen
kernel = np.array([[0, -1, 0],  
                   [-1, 5, -1],
                   [0, -1, 0]])
sharpened = cv2.filter2D(src, -1, kernel)
# cv2.imshow("Sharpened Image", sharpened)

#Black and White
im_gray = cv2.imread('./Data/Vanya.jpg', cv2.IMREAD_GRAYSCALE)
#cv2.imshow("gray",im_gray)

# display input and output image
cv2.imshow("filters",np.hstack((dst, median, sharpened)))
cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image
