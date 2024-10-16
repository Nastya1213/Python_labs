import numpy as np
import sys

def load_data(file_path):
    """
    Загружает список целых чисел из файла
    """
    return np.loadtxt(file_path, dtype=int)

def random_select(real_data, synthetic_data, P):
    """
    Перемешивает реальные и синтетические данные с вероятностью P.
     Если элемент меньше P, выбирается элемент из массива синтетических данных (synthetic_data),
       в противном случае — из реальных данных (real_data).
    """
    mask = np.random.rand(len(real_data)) < P
    return np.where(mask, synthetic_data, real_data)

def alternate_select(real_data, synthetic_data, P):
    """
    Второй способ перемешивания: Чередование с вероятностью замены.
    """
    start_with_synthetic = np.random.rand() < P
    alternating_pattern = np.tile([start_with_synthetic, not start_with_synthetic], len(real_data)//2 + 1)[:len(real_data)]

    return np.where(alternating_pattern, synthetic_data, real_data)

def main(file1, file2, P):
    # Загружаем данные из файлов
    real_data = load_data(file1)
    synthetic_data = load_data(file2)

    # Проверка, что длины массивов одинаковы
    if len(real_data) != len(synthetic_data):
        print("Ошибка: длины массивов в файлах должны совпадать!")
        return

    # Перемешивание первым способом
    print("Первый способ перемешивания:")
    mixed_data1 = random_select(real_data, synthetic_data, P)
    print(mixed_data1)

    # Перемешивание вторым способом
    print("\nВторой способ перемешивания:")
    mixed_data2 = alternate_select(real_data, synthetic_data, P)
    print(mixed_data2)

if __name__ == "__main__":
    # Получаем аргументы из командной строки
    if len(sys.argv) != 4:
        print("Использование: python3 random_select-1.py file1.txt file2.txt P")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    P = float(sys.argv[3])

    if not 0 <= P <= 1:
        print("Ошибка: вероятность P должна быть между 0 и 1")
        sys.exit(1)

    main(file1, file2, P)

