import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Загружаем изображение
image = cv2.imread('./Data/Vanya.jpg', cv2.IMREAD_UNCHANGED)

if image is None:
    print("Ошибка: изображение не найдено!")
    exit(1)

# Преобразуем изображение в формат RGB для matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
current_image = image_rgb.copy()  # Текущее изображение для отображения

# Создаем фигуру и оси
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.3)  # Оставляем место для слайдеров и кнопок
img_plot = ax.imshow(current_image)

# Оси для слайдеров и кнопок
ax_r = plt.axes([0.15, 0.05, 0.65, 0.03]) 
ax_g = plt.axes([0.15, 0.10, 0.65, 0.03]) 
ax_b = plt.axes([0.15, 0.15, 0.65, 0.03]) 
ax_gaus = plt.axes([0.05, 0.6, 0.15, 0.05]) 
ax_bw = plt.axes([0.05, 0.5, 0.15, 0.05])  
ax_res = plt.axes([0.05, 0.4, 0.15, 0.05]) 
ax_mb = plt.axes([0.05, 0.7, 0.15, 0.05]) 
ax_sh = plt.axes([0.05, 0.8, 0.15, 0.05]) 

# Создаем слайдеры для RGB-каналов
axcolor = 'lightgoldenrodyellow'
s_r = Slider(ax_r, label="Red", valmin=0, valmax=255, valinit=0)
s_g = Slider(ax_g, label="Green", valmin=0, valmax=255, valinit=0)
s_b = Slider(ax_b, label="Blue", valmin=0, valmax=255, valinit=0)

# Создаем кнопки
b_gf = Button(ax_gaus, 'GaussianBlur') 
b_bw = Button(ax_bw, 'Black&White') 
b_res = Button(ax_res, 'Reset')
b_mb = Button(ax_mb, 'MedianBlur')
b_sh = Button(ax_sh, 'Sharpening')

def update(val):
    """Обновляем изображение при изменении слайдеров."""
    r = s_r.val
    g = s_g.val
    b = s_b.val

    # Применяем сдвиг по каналам
    rgb_shift = np.array([r, g, b], dtype=np.int32)
    result = current_image.astype(np.int32) + rgb_shift
    result = np.clip(result, 0, 255).astype(np.uint8)

    # Обновляем изображение
    img_plot.set_data(result)
    fig.canvas.draw_idle()


def apply_sharpening(event):
    global current_image
    kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
    sharpened = cv2.filter2D(image_rgb, -1, kernel)
    current_image = sharpened
    img_plot.set_data(current_image)
    fig.canvas.draw_idle()



def apply_median_blur(event):
    global current_image
    median = cv2.medianBlur(image_rgb, 5)
    current_image = median
    img_plot.set_data(current_image)
    fig.canvas.draw_idle()


def apply_gaussian_blur(event):
    global current_image
    blurred = cv2.GaussianBlur(image_rgb, (5, 5), 0)
    current_image = blurred
    img_plot.set_data(current_image)
    fig.canvas.draw_idle()

def apply_black_and_white(event):
    global current_image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bw_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)  # Преобразуем обратно в RGB
    current_image = bw_image
    img_plot.set_data(current_image)
    fig.canvas.draw_idle()

def reset_image(event):
    global current_image
    current_image = image_rgb.copy()
    img_plot.set_data(current_image)
    fig.canvas.draw_idle()

# Привязываем действия к слайдерам и кнопкам
s_r.on_changed(update)
s_g.on_changed(update)
s_b.on_changed(update)

b_gf.on_clicked(apply_gaussian_blur)
b_bw.on_clicked(apply_black_and_white)
b_res.on_clicked(reset_image)
b_mb.on_clicked(apply_median_blur)
b_sh.on_clicked(apply_sharpening)

# Отображаем окно
plt.show()
