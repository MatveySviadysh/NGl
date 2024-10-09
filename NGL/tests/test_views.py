import pytest # type: ignore
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import Tutor 
from mybot.models import SupportMessage
#from user.forms import UserProfileForm 
from user.models import UserProfile, Review


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

    response = client.post(reverse('login-user'), {
        'username': 'testuser',
        'password': 'testpassword123',
    })
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_logout(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    response = client.get(reverse('logout-user'))
    assert response.status_code == 302
    assert not response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_profile(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    response = client.get(reverse('profile-user'))
    assert response.status_code == 200
    assert 'user' in response.context
    assert response.context['user'] == user

@pytest.mark.django_db
def test_register_tutor(client):
    registration_data = {
        'email': 'testtutor@example.com',
        'password': 'testpasswordWORD123',
        'password_confirm': 'testpasswordWORD123',
        'full_name': 'Test Tutor',
        'phone_number': '+375291234567',
        'specialization': 'Math',
    }
    response = client.post(reverse('register_tutor'), registration_data)
    assert response.status_code == 302
    assert Tutor.objects.count() == 1
    tutor = Tutor.objects.get(email='testtutor@example.com')
    assert tutor.full_name == 'Test Tutor'
    assert tutor.phone_number == '+375291234567'

@pytest.mark.django_db
def test_login_tutor(client):
    tutor = Tutor.objects.create_user(
        email='testtutor@example.com',
        password='testpassword123',
        full_name='Test Tutor',
        phone_number='+375291234567',
        specialization='Math'
    )
    response = client.post(reverse('login_tutor'), {
        'email': 'testtutor@example.com',
        'password': 'testpassword123',
    })
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated
    assert response.url == reverse('profile-tutor', kwargs={'full_name': tutor.full_name})

# @pytest.mark.django_db
# def test_tutor_logout(client):
#     tutor = Tutor.objects.create_user(
#         email='testtutor@example.com',
#         password='testpassword123',
#         full_name='Test Tutor',
#         phone_number='+375291234567',
#         specialization='Math'
#     )
#     client.login(email='testtutor@example.com', password='testpassword123')
#     response = client.post(reverse('logout-tutor'))
#     assert response.url == reverse('main-page')


@pytest.mark.django_db
def test_change_password_user(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    new_password_data = {
        'old_password': 'testpassword123',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'newpasswordWORD123'
    }
    response = client.post(reverse('change-password-user'), new_password_data)
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated
    response_login = client.post(reverse('login-user'), {
        'username': 'testuser',
        'password': 'newpasswordWORD123',
    })
    assert response_login.status_code == 302
    assert response_login.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_change_password_user_success(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    new_password_data = {
        'old_password': 'testpassword123',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'newpasswordWORD123'
    }
    response = client.post(reverse('change-password-user'), new_password_data)
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated
    response_login = client.post(reverse('login-user'), {
        'username': 'testuser',
        'password': 'newpasswordWORD123',
    })
    assert response_login.status_code == 302
    assert response_login.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_change_password_user_wrong_old_password(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    new_password_data = {
        'old_password': 'wrong_old_password',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'newpasswordWORD123'
    }
    response = client.post(reverse('change-password-user'), new_password_data)
    assert response.status_code == 200
    assert 'old_password' in response.context['form'].errors

@pytest.mark.django_db
def test_change_password_user_passwords_do_not_match(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    new_password_data = {
        'old_password': 'testpassword123',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'different_new_password'
    }
    response = client.post(reverse('change-password-user'), new_password_data)
    assert response.status_code == 200 
    assert 'new_password2' in response.context['form'].errors

@pytest.mark.django_db
def test_change_password_user_empty_fields(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    new_password_data = {
        'old_password': '',
        'new_password1': '',
        'new_password2': ''
    }
    response = client.post(reverse('change-password-user'), new_password_data)
    assert response.status_code == 200
    assert 'old_password' in response.context['form'].errors
    assert 'new_password1' in response.context['form'].errors

User = get_user_model()

@pytest.mark.django_db
def test_button_page_get(client):
    url = reverse('button_page') 
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.content.decode()  
    assert '<h1>Support Message</h1>' in response.content.decode() 

@pytest.mark.django_db
def test_button_page_post_valid(client):
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    url = reverse('button_page')
    response = client.post(url, {'message': 'This is a test support message'})

    assert response.status_code == 302 
    assert SupportMessage.objects.count() == 1
    assert SupportMessage.objects.first().message == 'This is a test support message'
    assert response.url == reverse('main-page')

@pytest.mark.django_db
def test_button_page_post_invalid(client):
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    url = reverse('button_page')
    response = client.post(url, {'message': ''}) 

    assert response.status_code == 200 
    assert SupportMessage.objects.count() == 0 
    assert 'form' in response.content.decode() 
    assert 'This field is required.' in response.content.decode() 

@pytest.mark.django_db
def test_button_page_post_not_logged_in(client):
    url = reverse('button_page')
    response = client.post(url, {'message': 'I should not be able to submit'})

    assert response.status_code == 302  
    assert response.url == reverse('login-user') 

@pytest.mark.django_db
def test_support_message_detail_get(client):
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
    message = SupportMessage.objects.create(name=user.username, message='Test message')
    
    url = reverse('support_message_detail', args=[message.id])
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'message' in response.context
    assert 'response_form' in response.context
    assert message.message in response.content.decode()

@pytest.mark.django_db
def test_support_message_detail_post_valid(client):
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    message = SupportMessage.objects.create(name=user.username, message='Test message')
    url = reverse('support_message_detail', args=[message.id])
    response = client.post(url, {'message': 'Updated message'})
    assert response.status_code == 302
    assert response.url == reverse('admin:mybot_supportmessage_changelist')

@pytest.mark.django_db
def test_support_message_detail_post_invalid(client):
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    message = SupportMessage.objects.create(name=user.username, message='Test message')
    url = reverse('support_message_detail', args=[message.id])
    response = client.post(url, {'message': ''})
    assert response.status_code == 302
    assert response.url == '/admin/mybot/supportmessage/'
    message.refresh_from_db()
    assert message.message == 'Test message'

@pytest.mark.django_db
def test_support_message_detail_post_not_logged_in(client):
    message = SupportMessage.objects.create(name='testuser', message='Test message')
    url = reverse('support_message_detail', args=[message.id])
    
    # Пост неавторизованного клиента
    response = client.post(url, {'message': 'I should not be able to submit'})

    # Проверка перенаправления
    assert response.status_code == 302
    assert response.url == '/admin/mybot/supportmessage/'  # Обновите, если ваше приложение перенаправляет сюда

@pytest.mark.django_db  
def test_change_user_profile_get(client):
    # Create a user
    user = User.objects.create_user(username='testuser', password='testpassword123')

    # Create a UserProfile only if it doesn't exist
    UserProfile.objects.get_or_create(user=user, defaults={
        'description': 'Initial description', 
        'phone_number': '1234567890'
    })

    client.login(username='testuser', password='testpassword123')

    response = client.get(reverse('chenge_user_profile'))  # Adjust the URL name to your actual one
    assert response.status_code == 200
    assert 'form' in response.context
    profile = UserProfile.objects.get(user=user)
    assert response.context['form'].instance == profile  # Check that the form is initialized with the existing profile

@pytest.mark.django_db  
def test_change_user_profile_post_valid(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    profile, created = UserProfile.objects.get_or_create(user=user, defaults={
        'description': 'Initial description', 
        'phone_number': '1234567890'
    })
    client.login(username='testuser', password='testpassword123')

    update_data = {
        'description': 'Updated description',
        'phone_number': '0987654321'
    }
    response = client.post(reverse('chenge_user_profile'), update_data)

    assert response.status_code == 302  # Check for redirect after successful update
    profile.refresh_from_db()  # Refresh the profile instance from the database
    assert profile.description == 'Updated description'
    assert profile.phone_number == '0987654321'
    assert response.url == reverse('profile-user')  # Adjust the redirect URL to your actual one

User = get_user_model()

@pytest.mark.django_db
def test_profile_tutor_success(client):
    # Create a tutor for the test
    tutor = Tutor.objects.create_user(
        email='testtutor@example.com',
        password='testpassword123',
        full_name='Test Tutor',
        phone_number='+375291234567',
        specialization='Math'
    )
    
    # Log in as a user (if necessary, modify User creation based on your auth method)
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    response = client.get(reverse('profile-tutor', args=[tutor.full_name]))
    
    assert response.status_code == 200
    assert 'tutor' in response.context
    assert response.context['tutor'] == tutor
    assert response.context['user'] == user
    assert 'user/pages/ProfileTutor.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_profile_tutor_not_found(client):
    # Log in as a user
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    # Expecting a 404 for a non-existent tutor
    response = client.get(reverse('profile-tutor', args=['Non Existent Tutor']))
    
    assert response.status_code == 404
    assert 'user/pages/404.html' in [template.name for template in response.templates]

@pytest.fixture
def create_tutors(db):
    # Создание нескольких тьюторов для тестов
    Tutor.objects.create(
        full_name='Tutor One',
        phone_number='+12345678900',
        specialization='Mathematics',
        email='tutor1@example.com',
        tutor_id='TUTOR001',
        rating=4.5,
        experience='5 years',
        services='Math tutoring',
        price=50.0,
        verified=True
    )

    Tutor.objects.create(
        full_name='Tutor Two',
        phone_number='+10987654321',
        specialization='Physics',
        email='tutor2@example.com',
        tutor_id='TUTOR002',
        rating=4.8,
        experience='3 years',
        services='Physics tutoring',
        price=60.0,
        verified=False
    )

@pytest.mark.django_db
def test_all_tutors(client,create_tutors):
    # Логинимся как пользователь (если требуется)
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    # Делать GET-запрос на страницу всех тьюторов
    response = client.get(reverse('all_tutors'))  # Убедитесь, что URL-нейм правильный

    # Проверка успешного ответа
    assert response.status_code == 200

    # Проверка правильного шаблона
    assert 'user/pages/AllTutors.html' in [template.name for template in response.templates]

    # Проверка наличия списка тьюторов в контексте
    assert 'tutors' in response.context
    assert len(response.context['tutors']) == 2  # Ожидаем два тьютора

    # Проверка конкретных значений тьюторов
    assert response.context['tutors'][0].full_name == 'Tutor One'
    assert response.context['tutors'][1].full_name == 'Tutor Two'
    assert response.context['tutors'][0].specialization == 'Mathematics'
    assert response.context['tutors'][1].specialization == 'Physics'
    assert response.context['tutors'][0].price == 50.0
    assert response.context['tutors'][1].price == 60.0
    assert response.context['tutors'][0].verified is True
    assert response.context['tutors'][1].verified is False



@pytest.mark.django_db
def test_tutor_list_search(client, create_tutors):
    # Тест с поиском по специализации 'Math'
    response = client.get(reverse('tutor-list-serarch'), {'query': 'Math'})

    # Проверка успешного ответа
    assert response.status_code == 200
    assert 'user/pages/TutorsList.html' in [template.name for template in response.templates]
    
    # Проверка наличия списка тьюторов в контексте
    assert 'tutors' in response.context
    assert len(response.context['tutors']) == 1  # Ожидаем, что найден один тьютор
    assert response.context['tutors'][0].full_name == 'Tutor One'
    assert response.context['query'] == 'Math'

    # Тест с пустым запросом
    response_empty = client.get(reverse('tutor-list-serarch'), {'query': ''})
    
    # Проверка успешного ответа
    assert response_empty.status_code == 200
    assert len(response_empty.context['tutors']) == 0
    assert response_empty.context['query'] == ''

@pytest.fixture
def user(db):
    # Создание пользователя для теста
    return User.objects.create_user(username='testuser', password='password')

@pytest.mark.django_db
def test_review_create_success(client, user):
    # Авторизация пользователя
    client.login(username='testuser', password='password')

    # Данные для нового отзыва
    data = {
        'comment': 'Great service!',
        'rating': 5
    }

    # Отправка POST-запроса для создания отзыва
    response = client.post(reverse('review_create'), data)

    # Проверка успешного создания отзыва
    assert response.status_code == 302  # 302 Redirect
    assert Review.objects.count() == 1  # Проверяем, что отзыв создан
    review = Review.objects.first()
    assert review.username == 'testuser'
    assert review.comment == 'Great service!'

def test_review_create_invalid_form(client, user):
    # Авторизация пользователя
    client.login(username='testuser', password='password')

    # Отправка POST-запроса с некорректными данными
    data = {
        'comment': '',  # Пустое поле, если контент обязательный
        'rating': 6  # Предположим, что рейтинг должен быть от 1 до 5
    }
    
    response = client.post(reverse('review_create'), data)

    # Проверка на ошибку формы
    assert response.status_code == 200  # Вернемся на ту же страницу с ошибками
    assert Review.objects.count() == 0  # Отзыв не создан
    assert 'form' in response.context  # Проверяем, что форма передана в контекст
    assert response.context['form'].errors  # Проверяем, что есть ошибки в форме


