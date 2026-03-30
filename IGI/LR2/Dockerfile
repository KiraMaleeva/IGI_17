# Используем выбранный образ
FROM python:3.9-slim

# Создаем рабочую директорию
WORKDIR /app

# Копируем библиотеку
COPY geometric_lib/ /app/geometric_lib/

# Копируем скрипт
COPY script.py /app/

# Запускаем скрипт (аргументы будем передавать при запуске)
ENTRYPOINT ["python", "script.py"]