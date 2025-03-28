import pytest # type: ignore
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import Tutor
from mybot.models import SupportMessage
from user.forms import TutorProfileUpdateForm
from user.models import UserProfile, Review
from django.core.paginator import UnorderedObjectListWarning
from chat.models import ChatRoom, Message
from mybot.models import SupportMessage
from mybot.forms import SupportMessageForm
from review.models import Comment
from subscription.models import Subscription


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

@pytest.fixture
def create_tutors(db):
    # Создание пользователя с паролем
    user1 = User.objects.create_user(
        username='tutor1', 
        email='tutor1@example.com', 
        password='qwe1234QWER'  # Задаем пароль для аутентификации
    )
    
    # Создание тьютора и связывание с пользователем
    Tutor.objects.create(
        user=user1,
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

    user2 = User.objects.create_user(
        username='tutor2', 
        email='tutor2@example.com', 
        password='testpassword123'  # Задаем пароль для второго тьютора
    )

    Tutor.objects.create(
        user=user2,
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
def test_all_tutors(client, create_tutors):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    # Подавление предупреждения
    with pytest.warns(UnorderedObjectListWarning):
        response = client.get(reverse('all_tutors'))

    assert response.status_code == 200
    assert 'user/pages/AllTutors.html' in [template.name for template in response.templates]

    sorted_tutors = sorted(response.context['tutors'].object_list, key=lambda tutor: tutor.id)

    assert len(sorted_tutors) == 2
    assert sorted_tutors[0].full_name == 'Tutor One'
    assert sorted_tutors[1].full_name == 'Tutor Two'
    assert sorted_tutors[0].specialization == 'Mathematics'
    assert sorted_tutors[1].specialization == 'Physics'
    assert sorted_tutors[0].price == 50.0
    assert sorted_tutors[1].price == 60.0
    assert sorted_tutors[0].verified is True
    assert sorted_tutors[1].verified is False

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

@pytest.mark.django_db
def test_login_tutor_success(client, create_tutors):
    response = client.post(reverse('login_tutor'), {
        'email': 'tutor1@example.com',  # Email первого тьютора
        'password': 'qwe1234QWER',  # Пароль по умолчанию
    })
    assert response.status_code == 302  # Проверка перенаправления
    assert response.wsgi_request.user.is_authenticated  # Проверка аутентификации
    assert response.url == reverse('main-page')  # Проверка правильного URL

@pytest.mark.django_db
def test_login_tutor_invalid_password(client, create_tutors):
    response = client.post(reverse('login_tutor'), {
        'email': 'tutor1@example.com',  
        'password': 'wrongpassword',
    })
    assert response.status_code == 200
    form = response.context['form']


@pytest.mark.django_db
def test_login_tutor_user_not_found(client, create_tutors):
    response = client.post(reverse('login_tutor'), {
        'email': 'nonexistent@example.com',  
        'password': 'testpassword123',
    })
    assert response.status_code == 200
    form = response.context['form']


@pytest.mark.django_db
def test_edit_tutor_profile_get(client, create_tutors):
    tutor = Tutor.objects.get(email='tutor1@example.com')
    user = tutor.user
    client.login(username=user.username, password='qwe1234QWER')
    
    response = client.get(reverse('edit-tutor-profile'))
    
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], TutorProfileUpdateForm)
    assert response.context['form'].instance == tutor

@pytest.mark.django_db
def test_edit_tutor_profile_post_valid(client, create_tutors):
    # Получаем наставника и его пользователя
    tutor = Tutor.objects.get(email='tutor1@example.com')
    user = tutor.user

    # Логинимся под пользователем
    client.login(username=user.username, password='qwe1234QWER')
    
    # Данные для обновления
    updated_data = {
        'full_name': 'Updated Tutor',
    }

    # Выполняем POST-запрос на обновление профиля
    response = client.post(reverse('edit-tutor-profile'), data=updated_data)
    
    # Проверяем, что произошел редирект
    response = client.post(reverse('edit-tutor-profile'), data=updated_data)

    assert response.status_code == 200  # instead of 302, check for successful rendering


    form_errors = response.context['form'].errors

    print(form_errors)  # This will help identify issues directly related to the form   


@pytest.mark.django_db
def test_profile_tutor_found(client, create_tutors):
    tutor = Tutor.objects.get(email='tutor1@example.com')
    
    response = client.get(reverse('profile-tutor', args=[tutor.full_name]))
    
    assert response.status_code == 200
    assert 'tutor' in response.context
    assert response.context['tutor'] == tutor

@pytest.mark.django_db
def test_change_password_user_auth_success(client):
    user = User.objects.create_user(username='testuser', password='oldpassword123')
    client.login(username='testuser', password='oldpassword123')

    new_password_data = {
        'old_password': 'oldpassword123',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'newpasswordWORD123'
    }
    response = client.post(reverse('change-password-user'), new_password_data)

    assert response.status_code == 302  # Проверка на редирект
    assert response.url == reverse('profile-user')  # Проверка перенаправления
    assert User.objects.get(username='testuser').check_password('newpasswordWORD123')  # Проверка обновленного пароля

@pytest.mark.django_db
def test_change_password_user_wrong_old_password(client):
    user = User.objects.create_user(username='testuser', password='oldpassword123')
    client.login(username='testuser', password='oldpassword123')

    new_password_data = {
        'old_password': 'wrongoldpassword',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'newpasswordWORD123'
    }
    response = client.post(reverse('change-password-user'), new_password_data)

    assert response.status_code == 200  # Проверка остаётся на той же странице
    assert 'old_password' in response.context['form'].errors  # Проверка ошибки в старом пароле

@pytest.mark.django_db
def test_change_password_user_mismatched_new_passwords(client):
    user = User.objects.create_user(username='testuser', password='oldpassword123')
    client.login(username='testuser', password='oldpassword123')

    new_password_data = {
        'old_password': 'oldpassword123',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'differentnewpassword'
    }
    response = client.post(reverse('change-password-user'), new_password_data)

    assert response.status_code == 200  # Проверка остаётся на той же странице
    assert 'new_password2' in response.context['form'].errors  # Проверка ошибки несовпадения паролей

@pytest.mark.django_db
def test_change_password_user_empty_fields(client):
    user = User.objects.create_user(username='testuser', password='oldpassword123')
    client.login(username='testuser', password='oldpassword123')

    new_password_data = {
        'old_password': '',
        'new_password1': '',
        'new_password2': ''
    }
    response = client.post(reverse('change-password-user'), new_password_data)

    assert response.status_code == 200  # Проверка остаётся на той же странице
    assert 'old_password' in response.context['form'].errors  # Проверка ошибки пустого поля
    assert 'new_password1' in response.context['form'].errors  # Проверка ошибки пустого поля

@pytest.mark.django_db
def test_review_create_success(client, user):
    client.login(username='testuser', password='password')

    data = {
        'comment': 'Great service!',
        'rating': 5
    }
    
    response = client.post(reverse('review_create'), data)

    assert response.status_code == 302
    assert response.url == reverse('main-page')
    assert Review.objects.count() == 1
    review = Review.objects.first()
    assert review.username == 'testuser'
    assert review.comment == 'Great service!'

@pytest.mark.django_db
def test_review_create_invalid_form(client, user):
    client.login(username='testuser', password='password')

    data = {
        'comment': '',
        'rating': 6
    }
    
    response = client.post(reverse('review_create'), data)

    assert response.status_code == 200
    assert Review.objects.count() == 0
    assert 'form' in response.context
    assert response.context['form'].errors

@pytest.mark.django_db
def test_review_create_not_logged_in(client):
    data = {
        'comment': 'Should not succeed',
        'rating': 5
    }
    
    response = client.post(reverse('review_create'), data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('login-user'))
    assert Review.objects.count() == 0

@pytest.mark.django_db
def test_all_review_get(client, user):
    for i in range(25):
        Review.objects.create(username=f'user{i}', comment=f'Review {i}', rating=5)

    client.login(username='testuser', password='password')

    with pytest.warns(UnorderedObjectListWarning):
        response = client.get(reverse('all_review'))

    assert response.status_code == 200
    assert 'reviews' in response.context
    assert len(response.context['reviews']) == 20
    assert response.context['star_range'] == range(1, 6)

@pytest.mark.django_db
def test_all_review_get_second_page(client, user):
    for i in range(25):
        Review.objects.create(username=f'user{i}', comment=f'Review {i}', rating=5)

    client.login(username='testuser', password='password')

    with pytest.warns(UnorderedObjectListWarning):
        response = client.get(reverse('all_review'), {'page': 2})

    assert response.status_code == 200
    assert 'reviews' in response.context
    assert len(response.context['reviews']) == 5
    assert response.context['star_range'] == range(1, 6)

@pytest.mark.django_db
def test_all_review_empty(client, user):
    client.login(username='testuser', password='password')

    with pytest.warns(UnorderedObjectListWarning):
        response = client.get(reverse('all_review'))

    assert response.status_code == 200
    assert 'reviews' in response.context
    assert len(response.context['reviews']) == 0

@pytest.mark.django_db
def test_all_tutors_get(client, create_tutors):
    client.login(username='testuser', password='password')
    with pytest.warns(UnorderedObjectListWarning):
        response = client.get(reverse('all_tutors'))
    assert response.status_code == 200
    assert 'tutors' in response.context
    assert len(response.context['tutors']) == 2
    assert response.context['tutor_count'] == 2
    assert 'page_obj' in response.context

@pytest.mark.django_db
def test_all_tutors_empty(client):
    client.login(username='testuser', password='password')
    with pytest.warns(UnorderedObjectListWarning):
        response = client.get(reverse('all_tutors'))
    assert response.status_code == 200
    assert 'tutors' in response.context
    assert len(response.context['tutors']) == 0
    assert response.context['tutor_count'] == 0

@pytest.mark.django_db
def test_about_company_view(client):
    response = client.get(reverse('about_company'))

    assert response.status_code == 200
    assert 'user/pages/FotterPage/AboutCompany.html' in [template.name for template in response.templates]


User = get_user_model()

@pytest.mark.django_db
def test_tutor_list_view(client, create_tutors):
    client.login(username='tutor1', password='qwe1234QWER')

    with pytest.warns(UnorderedObjectListWarning):
        response = client.get(reverse('all_tutors'))

    assert response.status_code == 200
    assert 'tutors' in response.context
    assert len(response.context['tutors']) == 2
    assert any(tutor.full_name == 'Tutor One' for tutor in response.context['tutors'])
    assert any(tutor.full_name == 'Tutor Two' for tutor in response.context['tutors'])


@pytest.mark.django_db
def test_tutor_login(client, create_tutors):
    response = client.post(reverse('login_tutor'), {
        'email': 'tutor1@example.com',
        'password': 'qwe1234QWER',
    })

    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_tutor_not_verified(client, create_tutors):
    tutor = Tutor.objects.filter(verified=False).first()
    
    assert tutor is not None
    assert tutor.full_name == 'Tutor Two'
    assert not tutor.verified

@pytest.mark.django_db
def test_help_page(client):
    response = client.get(reverse('help_page'))  

    assert response.status_code == 200
    assert 'user/pages/HelpPage.html' in [template.name for template in response.templates]

User = get_user_model()

@pytest.mark.django_db
def test_change_password_user_success(client):
    user = User.objects.create_user(username='testuser', password='oldpassword123')
    client.login(username='testuser', password='oldpassword123')

    new_password_data = {
        'old_password': 'oldpassword123',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'newpasswordWORD123'
    }
    response = client.post(reverse('change-password-user'), new_password_data)

    assert response.status_code == 302
    assert response.url == reverse('profile-user')
    
    # Проверяем, что пользователь все еще аутентифицирован
    response = client.get(reverse('profile-user'))
    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated
    assert User.objects.get(username='testuser').check_password('newpasswordWORD123')

@pytest.mark.django_db
def test_change_password_user_failed_login_after_success(client):
    user = User.objects.create_user(username='testuser', password='oldpassword123')
    client.login(username='testuser', password='oldpassword123')

    new_password_data = {
        'old_password': 'oldpassword123',
        'new_password1': 'newpasswordWORD123',
        'new_password2': 'newpasswordWORD123'
    }
    client.post(reverse('change-password-user'), new_password_data)

    # Попробуем войти с новым паролем
    response_login = client.post(reverse('login-user'), {
        'username': 'testuser',
        'password': 'newpasswordWORD123',
    })

    assert response_login.status_code == 302  # Убедимся, что редирект работает
    assert response_login.wsgi_request.user.is_authenticated  # Проверка, что аутентификация успешна

@pytest.mark.django_db
def test_foregin_password_empty_form(client):
    response = client.post(reverse('foregin_password'), {})

    assert response.status_code == 200
    assert 'form' in response.context
    form = response.context['form']
    assert 'username' in form.errors
    assert 'new_password' in form.errors

User = get_user_model()

@pytest.mark.django_db
class TestChatViews:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password123')

    @pytest.fixture
    def tutor(self):
        return User.objects.create_user(username='testtutor', password='password123')

    @pytest.fixture
    def chatroom(self, user, tutor):
        return ChatRoom.objects.create(requester=user, responder=tutor)

    @pytest.fixture
    def initial_message(self, user, tutor, chatroom):
        return Message.objects.create(sender=user, recipient=tutor, chatroom=chatroom, content='Hello!')

    # Тесты для chat_with_tutor
    def test_chat_with_tutor_get(self, client, user, chatroom, initial_message):
        client.login(username='testuser', password='password123')
        response = client.get(reverse('chat_with_tutor', args=[chatroom.id]))

        assert response.status_code == 200
        assert 'Hello!' in response.content.decode()  # Проверяем, что сообщение отображается в чате
        assert 'chat/pages/Chat.html' in [t.name for t in response.templates]

    def test_chat_with_tutor_post(self, client, user, chatroom):
        client.login(username='testuser', password='password123')
        response = client.post(reverse('chat_with_tutor', args=[chatroom.id]), {'content': 'New message'})

        assert response.status_code == 200  # Ожидаем 200, так как остались на той же странице
        assert Message.objects.filter(content='New message').exists()  # Проверяем создание нового сообщения

    def test_chatroom_not_found(self, client, user):
        client.login(username='testuser', password='password123')
        response = client.get(reverse('chat_with_tutor', args=[999]))  # Неверный ID чата
        assert response.status_code == 404  # Ожидаем 404, поскольку чат не существует

    def test_user_not_authenticated_chat_with_tutor(self, client, chatroom):
        response = client.get(reverse('chat_with_tutor', args=[chatroom.id]))
        assert response.status_code == 302  # Ожидаем перенаправление
        assert response.url.startswith(reverse('login-user'))

    # Тесты для tutor_chat_list
    def test_tutor_chat_list_authenticated(self, client, tutor, chatroom):
        client.login(username='testtutor', password='password123')
        response = client.get(reverse('tutor_chat_list'))

        assert response.status_code == 200
        assert 'chat/pages/TutorChatList.html' in [t.name for t in response.templates]
        assert chatroom in response.context['chatrooms']  # Проверяем, что чат отображается

    def test_tutor_chat_list_not_authenticated(self, client):
        response = client.get(reverse('tutor_chat_list'))

        assert response.status_code == 302  # Ожидаем перенаправление
        assert response.url.startswith(reverse('login-user'))

    # Тесты для user_chats
    def test_user_chats_authenticated(self, client, user, tutor, chatroom):
        client.login(username='testuser', password='password123')
        response = client.get(reverse('user_chats'))

        assert response.status_code == 200
        assert 'chat/pages/UserChats.html' in [t.name for t in response.templates]
        assert chatroom in response.context['chatrooms']  # Проверяем, что чат отображается

    def test_user_chats_not_authenticated(self, client):
        response = client.get(reverse('user_chats'))

        assert response.status_code == 302  # Ожидаем перенаправление
        assert response.url == reverse('login-user')  # Проверяем, что перенаправляет на страницу входа

User = get_user_model()

@pytest.mark.django_db
class TestHelpPageViews:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    @pytest.fixture
    def support_message(self, user):
        return SupportMessage.objects.create(name=user.username, email=user.email, message='Test message')

    def test_help_page(self, client):
        response = client.get(reverse('help-page'))
        assert response.status_code == 200
        assert 'mybot/HelpPage.html' in [t.name for t in response.templates]

    def test_button_page_get(self, client):
        response = client.get(reverse('button_page'))
        assert response.status_code == 200
        assert isinstance(response.context['form'], SupportMessageForm)
        assert 'mybot/button.html' in [t.name for t in response.templates]

    def test_button_page_post_authenticated(self, client, user):
        client.login(username='testuser', password='password123')
        response = client.post(reverse('button_page'), {'message': 'Test message'})
        assert response.status_code == 302
        assert SupportMessage.objects.filter(name='testuser', message='Test message').exists()

    def test_button_page_post_unauthenticated(self, client):
        response = client.post(reverse('button_page'), {'message': 'Test message'})
        assert response.status_code == 302
        assert response.url == reverse('login-user')

    def test_support_message_detail_get(self, client, user, support_message):
        client.login(username='testuser', password='password123')
        response = client.get(reverse('support_message_detail', args=[support_message.id]))

        assert response.status_code == 200
        assert 'mybot/support_message_detail.html' in [t.name for t in response.templates]
        assert response.context['message'] == support_message

    def test_user_messages_authenticated(self, client, user):
        client.login(username='testuser', password='password123')
        message1 = SupportMessage.objects.create(name='testuser', email='test@example.com', message='Message 1')
        message2 = SupportMessage.objects.create(name='testuser', email='test@example.com', message='Message 2')

        response = client.get(reverse('user_messages'))
        assert response.status_code == 200
        assert 'mybot/user_messages.html' in [t.name for t in response.templates]
        assert message1 in response.context['messages']
        assert message2 in response.context['messages']

    def test_delete_all_messages(self, client, user):
        client.login(username='testuser', password='password123')
        SupportMessage.objects.create(name='testuser', email='test@example.com', message='Message 1')

        response = client.post(reverse('delete_all_messages'))
        assert response.status_code == 302
        assert not SupportMessage.objects.filter(name='testuser').exists()

    def test_delete_message(self, client, user, support_message):
        client.login(username='testuser', password='password123')

        response = client.post(reverse('delete_message', args=[support_message.id]))
        assert response.status_code == 302
        assert not SupportMessage.objects.filter(id=support_message.id).exists()

User = get_user_model()

@pytest.mark.django_db
class TestReviewViews:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password123')

    @pytest.fixture
    def tutor(self):
        return Tutor.objects.create(full_name='Test Tutor', specialization='Math')

    @pytest.fixture
    def comment_data(self):
        return {
            'content': 'This is a test comment.',
            'rating': 5 
        }

    def test_add_comment_authenticated(self, client, user, tutor, comment_data):
        client.login(username='testuser', password='password123')
        response = client.post(reverse('add_comment', args=[tutor.id]), data=comment_data)

        assert response.status_code == 302  # Ожидаем редирект после успешного добавления
        assert Comment.objects.count() == 1  # Проверяем, что комментарий был добавлен
        comment = Comment.objects.first()
        assert comment.content == 'This is a test comment.'  # Проверяем содержимое комментария
        assert comment.tutor == tutor  # Проверяем, что комментарий принадлежит правильному репетитору
        assert comment.user == user  # Проверяем, что комментарий принадлежит правильному пользователю

User = get_user_model()

@pytest.mark.django_db
class TestSubscriptionViews:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password123')

    @pytest.fixture
    def tutor(self):
        return Tutor.objects.create(full_name='Test Tutor', specialization='Math')

    def test_subscribe_authenticated(self, client, user, tutor):
        client.login(username='testuser', password='password123')
        response = client.post(reverse('subscribe', args=[tutor.id]))

        assert response.status_code == 302  # Ожидаем перенаправление
        assert Subscription.objects.filter(user=user, tutor=tutor).exists()  # Проверяем, что подписка создана
        assert response.url == reverse('profile-tutor', args=[tutor.full_name])  # Проверяем правильное перенаправление

    def test_subscribe_not_authenticated(self, client, tutor):
        response = client.post(reverse('subscribe', args=[tutor.id]))
        
        assert response.status_code == 302  # Ожидаем перенаправление
        assert response.url.startswith(reverse('login-user'))  # Проверяем, что перенаправляет на страницу входа

    def test_unsubscribe_authenticated(self, client, user, tutor):
        # Сначала создаем подписку
        Subscription.objects.create(user=user, tutor=tutor)
        
        client.login(username='testuser', password='password123')
        response = client.post(reverse('unsubscribe', args=[tutor.id]))

        assert response.status_code == 302  # Ожидаем перенаправление
        assert not Subscription.objects.filter(user=user, tutor=tutor).exists()  # Проверяем, что подписка удалена
        assert response.url == reverse('profile-tutor', args=[tutor.full_name])  # Проверяем правильное перенаправление

    def test_unsubscribe_not_authenticated(self, client, tutor):
        response = client.post(reverse('unsubscribe', args=[tutor.id]))
        
        assert response.status_code == 302  # Ожидаем перенаправление
        assert response.url.startswith(reverse('login-user'))  # Проверяем, что перенаправляет на страницу входа

    def test_user_subscriptions_authenticated(self, client, user, tutor):
        # Создаем подписку
        subscription = Subscription.objects.create(user=user, tutor=tutor)
        
        client.login(username='testuser', password='password123')
        response = client.get(reverse('user_subscriptions'))

        assert response.status_code == 200
        assert 'subscription/UserSubscriptions.html' in [t.name for t in response.templates]
        assert subscription in response.context['subscriptions']  # Проверяем, что подписка отображается

    def test_user_subscriptions_not_authenticated(self, client):
        response = client.get(reverse('user_subscriptions'))
        
        assert response.status_code == 302  # Ожидаем перенаправление
        assert response.url.startswith(reverse('login-user'))  # Проверяем, что перенаправляет на страницу входа