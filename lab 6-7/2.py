import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
 
def nothing(x):
    pass

image = cv.imread('./Data/Vanya.jpg', cv.IMREAD_UNCHANGED)

if image is None:
    print("Ошибка: изображение не найдено!")
    exit(1)


cv.namedWindow('image')
# create trackbars for color change
cv.createTrackbar('R','image',0,255,nothing)
cv.createTrackbar('G','image',0,255,nothing)
cv.createTrackbar('B','image',0,255,nothing)
rgb_shift = [0, 0, 0]

while(1):
    # get current positions of four trackbars
    r = cv.getTrackbarPos('R','image')
    g = cv.getTrackbarPos('G','image')
    b = cv.getTrackbarPos('B','image')
    rgb_shift = [r, g, b]
    # Применяем сдвиг по каналам
    rgb_shift = np.array([b, g, r], dtype=np.int32)
    result = image.astype(np.int32) + rgb_shift  # Приводим к int32 для предотвращения переполнения
    result = np.clip(result, 0, 255).astype(np.uint8)  # Обрезаем значения до допустимого диапазона

    cv.imshow('image', result)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

 
cv.destroyAllWindows()
 
