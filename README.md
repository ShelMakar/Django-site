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
* ## **Создайте виртуальную среду**
    ##### Windows

    ```cmd
    python -m venv venv
    ```
    ##### Linux

    ```cmd
    sudo apt install python3-venv
    ```

* ## Активируем окружение коммандой
    ##### Windows

    ```cmd
    venv\scripts\activate
    ```
    ###### Linux

    ```cmd
    source ./venv/bin/activate
    ```

## Установка зависимостей из папки 'requirements'
```bash
pip install -r requirements/prod.txt
pip install -r requirements/dev.txt
pip install -r requirements/test.txt
```

# Миграции базы данных
> ##### Этот проект использует систему миграций для управления изменениями в структуре базы данных.

* ## Перейдем в каталог "lyceum"
    ```bash
    cd lyceum
    ```

* ## Для того чтобы создать миграцию
    ```bash
    python manage.py makemigrations
    ```

* ## Для того чтобы применить миграцию
    ```bash
    python manage.py migrate
    ```
* ## Для того чтобы загрузить фикстуры:
    ```python
    python manage.py loaddata fixtures/data.json
    ```

* ## Для того чтобы выгрузить фикстуры:
    ```python
    python -X utf8 manage.py dumpdata --indent 2 catalog > fixtures/data.json
    ```


## Для корректного запуска скопируйте файл config.env
```bash
cp config.env .env
```

## Ознакомиться с ER диаграммой можете ниже
![IMAGE_DESCRIPTION](https://gitlab.crja72.ru/django/2024/autumn/course/students/172544-makarshelyag-course-1187/blob/main/ER.jpg)
```
ER.jpg
```
## Для тестирования проекта используйте зависимости, установленные ранее и команду
```bash
python3 manage.py test
```
## В случае необходимости корректируйте и добавляйте свои тесты

## Чтобы перевест итест нужно создать конфигурацию локализации и заполнить ее содержимое
```bash
django-admin makemessages -l your_lang
```
## Чтобы скомпилировать, используйте следующуу команду
```bash
django-admin compilemessages
```
## Чтобы проверить перевод используйте команду, с кодом языка
```python
LANGUAGE_CODE = 'en-us'
```
## Запуск
```bash
cd lyceum
python3 manage.py runserver
```