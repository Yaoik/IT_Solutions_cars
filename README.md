## Getting started



1. Создайте виртуальное окружение
```bash
python -m venv .venv
```
2. Запустите базу данных
```bash
docker-compose up
```
3. Переключитесь на .venv
```bash
.venv\Scripts\activate.bat  
```
4. Установите зависимости
```bash
pip install -r requirements.txt
```
5. Выполните миграцию базы данных
```bash
python manage.py migrate
```
6. Запустить тесты
```bash
python manage.py test
```
7. Cоздайте администратора
```bash
python manage.py createsuperuser
```
8. Запустите сервер разработки
```bash
python manage.py runserver
```
9. Некоторые полезные страницы
   * Админка - http://127.0.0.1:8000/admin/
   * API документация
     * Swagger - http://127.0.0.1:8000/api/docs/swagger/
     * Redoc - http://127.0.0.1:8000/api/docs/redoc/
