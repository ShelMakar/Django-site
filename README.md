## ативация виртуального окружения
``` bash
python3 -m venv venv
source venv/bin/activate
```

## установка зависимостей из папки 'requirements'
``` bash
pip install -r prod.txt
pip install -r dev.txt
pip install -r test.txt
```

## для корретного запуска скопируйте файл config.env
``` bash
cp config.env .env
```

## запуск
``` bash
cd lyceum
python3 manage.py runserver
```