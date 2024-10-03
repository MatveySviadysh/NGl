import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import Tutor 

User = get_user_model()

@pytest.mark.django_db  
def test_register(client):
    assert User.objects.count() == 0
    response = client.post(reverse('register-user'), {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'testpasswordWORD123',
        'password2': 'testpasswordWORD123',
    })
    assert response.status_code == 302
    content = response.content.decode()
    assert User.objects.count() == 1
    assert response.url == reverse('profile-user')
    redirect_response = client.get(response.url)
    content = redirect_response.content.decode()
    assert 'error' not in content

@pytest.mark.django_db
def test_login(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')

    response = client.post(reverse('login-user'), {  # Измените на 'login-user'
        'username': 'testuser',
        'password': 'testpassword123',
    })
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_logout(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    response = client.get(reverse('logout-user'))  # Измените на 'logout-user'
    assert response.status_code == 302
    assert not response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_profile(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    response = client.get(reverse('profile-user'))  # Оставьте как есть
    assert response.status_code == 200
    assert 'user' in response.context
    assert response.context['user'] == user

@pytest.mark.django_db
def test_register_tutor(client):
    # Проверяем, что в начале нет репетиторов
    assert Tutor.objects.count() == 0

    # Данные для регистрации репетитора
    registration_data = {
        'email': 'testtutor@example.com',
        'password': 'testpasswordWORD123',
        'password_confirm': 'testpasswordWORD123',  # Поле для подтверждения пароля
        'full_name': 'Test Tutor',
        'phone_number': '+375291234567',
        'specialization': 'Math',
    }

    # Отправляем POST-запрос на регистрацию репетитора
    response = client.post(reverse('register_tutor'), registration_data)

    # Проверяем статус ответа и выводим ошибки, если не редирект
    if response.status_code != 302:
        print(response.context['form'].errors)

    # Проверяем, что произошел успешный редирект
    assert response.status_code == 302

    # Проверяем, что репетитор создан
    assert Tutor.objects.count() == 1
    tutor = Tutor.objects.get(email='testtutor@example.com')
    assert tutor.full_name == 'Test Tutor'
    assert tutor.phone_number == '+375291234567'

@pytest.mark.django_db
def test_login_tutor(client):
    # Создаем репетитора перед тестом
    tutor = Tutor.objects.create_user(
        email='testtutor@example.com',
        password='testpassword123',
        full_name='Test Tutor',
        phone_number='+375291234567',
        specialization='Math'
    )

    # Отправляем POST-запрос на вход репетитора
    response = client.post(reverse('login_tutor'), {
        'email': 'testtutor@example.com',
        'password': 'testpassword123',
    })

    # Проверяем, что репетитор был успешно залогинен и произошел редирект на страницу профиля
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated
    assert response.url == reverse('profile-tutor')

@pytest.mark.django_db
def test_tutor_logout(client):
    # Создаем и логиним репетитора
    tutor = Tutor.objects.create_user(
        email='testtutor@example.com',
        password='testpassword123',
        full_name='Test Tutor',
        phone_number='+375291234567',
        specialization='Math'
    )
    client.login(email='testtutor@example.com', password='testpassword123')

    # Отправляем POST-запрос на выход
    response = client.post(reverse('logout-tutor'))

    # Проверяем, что репетитор был успешно разлогинен
    assert response.status_code == 302
    assert not response.wsgi_request.user.is_authenticated
    assert response.url == reverse('main-page')


