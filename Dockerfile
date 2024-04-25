# Используйте официальный образ Python как базовый
FROM python:3.10.12

# Установите рабочую директорию в контейнере
WORKDIR /user/src/e-book

# Копируйте файлы зависимостей в контейнер
COPY ./requirements.txt /user/src/requirements.txt

# Обновление списка пакетов и установка зависимостей для mysqlclient
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установите зависимости Python
RUN pip install -r /user/src/requirements.txt
RUN pip install mysqlclient

# Копируйте проект в контейнер
COPY . /user/src/e-book/

# Откройте порт, который будет слушать ваше приложение
EXPOSE 8000

# Команда для запуска вашего приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
