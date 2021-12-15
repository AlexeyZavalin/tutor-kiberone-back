## Запуск проекта локально:
1. Выполняем миграции - python manage.py migrate
2. Загружаем фикстуры - python manage.py loaddata main_initial.json/fair_initial.json
3. Создаем необходимые переменные окружения (DJANGO_SETTINGS_MODULE=kiberone_tutor.local)
4. Запускаем проект - python manage.py runserver
5. Переходим в браузер на 127.0.0.1:8000

## Запуск проекта через docker-compose:
1. Выполняем команду - docker-compose up -d
2. Подключаемся к контейнеру web - docker exec -it web   
2. Переходим в браузер на localhost:8000
