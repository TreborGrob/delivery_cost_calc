FROM python:3.13-slim

# Настройка системных переменных
# ENV PYTHONUNBUFFERED=1
# Устанавливаем рабочую директорию
WORKDIR /amount_shipping

# Устанавливаем зависимости
COPY requirements.txt .
RUN python.exe -m pip install --upgrade pip
RUN python.exe -m pip install -r requirements.txt

# Копируем приложение
COPY tg_bot/ tg_bot/
COPY settings.py .
COPY main.py .

# Команда запуска
CMD ["python3", "main.py"]