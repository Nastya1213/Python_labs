import pandas as pd
import numpy as np

# Загрузка данных
titanic_with_labels = pd.read_csv("data/titanic_with_labels.csv", sep=' ')
cinema_sessions = pd.read_csv("data/cinema_sessions.csv", sep=' ')

# 1. Обработка пола (sex)
def process_sex(df):
    # Приводим значения пола к одному стандарту: "м" -> "male", "ж" -> "female", "M" -> "male"
    df['sex'] = df['sex'].str.lower().map({
        'м': 1, 'm': 1, 'ж': 0, 'f': 0
    })
    
    # Удаляем строки, где пол не указан или не удалось сопоставить
    df = df[df['sex'].notna()]
    
    return df

titanic_with_labels = process_sex(titanic_with_labels)

# 2. Обработка номеров рядов (row_number)
def fill_max_row(df):
    # Находим максимальный номер ряда
    max_row = df['row_number'].max()
    
    # Заполняем пропущенные значения максимальным номером ряда
    df['row_number'] = df['row_number'].fillna(max_row)
    
    return df

titanic_with_labels = fill_max_row(titanic_with_labels)

# 3. Обработка количества выпитого в литрах (liters_drunk)
def filter_liters(df):
    # Удаляем отрицательные значения и выбросы (например, больше 10 литров)
    mean_liters = df['liters_drunk'][(df['liters_drunk'] >= 0) & (df['liters_drunk'] <= 10)].mean()
    
    # Заменяем выбросы и отрицательные значения средним значением
    df['liters_drunk'] = np.where((df['liters_drunk'] < 0) | (df['liters_drunk'] > 10), mean_liters, df['liters_drunk'])
    
    return df

titanic_with_labels = filter_liters(titanic_with_labels)

# Приводим имена столбцов к нижнему регистру для согласованности
titanic_with_labels.columns = titanic_with_labels.columns.str.lower()
cinema_sessions.columns = cinema_sessions.columns.str.lower()

# 4. Объединение данных по столбцу check_number
merged_data = pd.merge(titanic_with_labels, cinema_sessions, on='check_number', how='inner')
titanic_with_labels = filter_liters(titanic_with_labels)

# 4. Обработка возраста (age) 
# TODO: 1 столбец 
def process_age(df):
    # Определяем условия для категорий
    conditions = [
        df['age'] < 18,
        (df['age'] >= 18) & (df['age'] <= 50),
        df['age'] > 50
    ]
    # Определяем значения, которые будут присвоены в новом столбце
    choices = ['child', 'adult', 'senior']
    # Создаем новый столбец age на основе условий
    df['age'] = np.select(conditions, choices, default='unknown')
    return df

titanic_with_labels = process_age(titanic_with_labels)

# 5. Обработка напитков (drink)
# TODO: Расширить бд
def process_drink(df):
    df['is_alcoholic'] = df['drink'].str.lower().map({
        'cola': 0,
        'fanta': 0,
        'beerbeer': 1,
        'bugbeer': 1,
        'water': 0,
        '"Strong beer"': 1


    })
     # Заполняем NaN (если напитка нет в словаре) значением -1
    df['is_alcoholic'] = df['is_alcoholic'].fillna(-1)  # или используйте 0 для безалкогольных
    
    return df

titanic_with_labels = process_drink(titanic_with_labels)

# 6. Обработка номера чека (check_number)
def process_check_number(df, sessions):
    # Преобразуем время сессий в категории
    def categorize_time(row):
        time = pd.to_datetime(row['session_start']).time()
        if time < pd.to_datetime("12:00:00").time():
            return 'morning'
        elif time < pd.to_datetime("18:00:00").time():
            return 'day'
        else:
            return 'evening'
    
    sessions['session_category'] = sessions.apply(categorize_time, axis=1)
    
    # Объединяем данные по check_number и создаем dummy-переменные
    merged_sessions = pd.get_dummies(sessions['session_category'], prefix='session', drop_first=True)
    df = df.merge(sessions[['check_number']], on='check_number', how='left').join(merged_sessions)
    
    return df

titanic_with_labels = process_check_number(titanic_with_labels, cinema_sessions)

# Приводим имена столбцов к нижнему регистру для согласованности
titanic_with_labels.columns = titanic_with_labels.columns.str.lower()
cinema_sessions.columns = cinema_sessions.columns.str.lower()

# 7. Объединение данных по столбцу check_number
merged_data = pd.merge(titanic_with_labels, cinema_sessions, on='check_number', how='inner')

# Сохраняем объединенные данные в CSV
merged_data.to_csv('merged_data.csv', index=False)

print("Данные обработаны и объединены. Результат сохранен в 'merged_data.csv'.")