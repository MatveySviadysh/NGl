# 📦 **NGL** 🚀 

NGL — платформа для поиска нужных вам специалистов онлайн. 🌐

## 🔧 Установка

1. Клонируйте репозиторий:
    ```
    git clone https://github.com/yourusername/yourproject.git
    cd NGL
    ```
---

## 💻 Использование

2. Запустите проект:
    ```
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
    ```
    
    ```
    sudo docker-compose build
    sudo docker-compose up
    sudo docker-compose exec web python manage.py migrate
    ```

    ```
    docker build -f Dockerfile.app -t ngl-app .
    docker run -d -p 8000:8000 ngl-app 
    ```

    ```
    Supervisor

    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl restart django
    ```
---

### 📋 Содержание:
- **Название проекта**: Название вашего проекта.
- **Описание**: NGL — платформа для поиска нужных вам специалистов онлайн.
- **Установка**: Шаги по установке и настройке проекта.
- **Использование**: Примеры команд для запуска проекта.
- **Функции**: Основные функциональные возможности вашего проекта.

---
