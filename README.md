## ПРОЕКТ ЯНДЕКС СПЕЦИАЛИЗАЦИИ
![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/172544-makarshelyag-course-1187/badges/main/pipeline.svg)

## Чтобы колонировать проект
На странице обзора проекта в правом верхнем углу выберите 'Код', затем скопируйте URL для 'клонирования с использованием HTTPS.'
Откройте терминал и перейдите в каталог, в который вы хотите клонировать файлы.
Выполните следующую команду. Git автоматически создаст папку с именем репозитория и загрузит в неё файлы.
```bash
git clone <copied URL>
``` 

## Для корректной работы скачайте Python версии 3.12
## Активация виртуального окружения
``` bash
python3 -m venv venv
source venv/bin/activate
```

## Установка зависимостей из папки 'requirements'
``` bash
pip install -r prod.txt
pip install -r dev.txt
pip install -r test.txt
```

## Для корректного запуска скопируйте файл config.env
``` bash
cp config.env .env
```

## Для тестирования проекта используйте зависимости, установленные ранее и команду
```bash
cd lyceum
python3 manage.py test
```
## В случае необходимости корректируйте и добавляйте свои тесты

## Запуск
``` bash
cd lyceum
python3 manage.py runserver
```