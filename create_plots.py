import matplotlib.pyplot as plt
from io import BytesIO


def create_temp_max_hist(data):
    plt.figure(figsize=(10, 6))  # Устанавливаем размер графика

    for city, values in data.items():
        plt.plot(values['day'], values['temp_max'], marker='o', label=city, linewidth=2)

    plt.title('Максимальная температура в день по выбранным городам')
    plt.xlabel('День')
    plt.ylabel('Температура (°C)')
    plt.grid(True)
    plt.legend()  # Добавляем легенду
    plt.xticks(rotation=45)  # Поворачиваем метки по оси X для лучшей читаемости
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer

def create_temp_min_hist(data):
    plt.figure(figsize=(10, 6))  # Устанавливаем размер графика

    for city, values in data.items():
        plt.plot(values['day'], values['temp_min'], marker='o', label=city, linewidth=2)

    plt.title('Минимальная температура в день по выбранным городам')
    plt.xlabel('День')
    plt.ylabel('Температура (°C)')
    plt.grid(True)
    plt.legend()  # Добавляем легенду
    plt.xticks(rotation=45)  # Поворачиваем метки по оси X для лучшей читаемости
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer

def create_rain_prob_hist(data):
    plt.figure(figsize=(10, 6))  # Устанавливаем размер графика

    for city, values in data.items():
        plt.plot(values['day'], values['rain_prob'], marker='o', label=city, linewidth=2)

    plt.title('Вероятнсть дождя в день по выбранным городам')
    plt.xlabel('День')
    plt.ylabel('Вероятность, %')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer

def create_wind_speed_hist(data):
    plt.figure(figsize=(10, 6))  # Устанавливаем размер графика

    for city, values in data.items():
        plt.plot(values['day'], values['wind_speed'], marker='o', label=city, linewidth=2)

    plt.title('Скорость ветра в день по выбранным городам')
    plt.xlabel('День')
    plt.ylabel('Скорость ветра, м/с')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer


def create_plots(data):
    return (
        create_temp_max_hist(data),
        create_temp_min_hist(data),
        create_rain_prob_hist(data),
        create_wind_speed_hist(data)
    )