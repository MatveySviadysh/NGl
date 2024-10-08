import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import Tutor 
from mybot.models import SupportMessage

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
    assert Tutor.objects.count() == 0
    registration_data = {
        'email': 'testtutor@example.com',
        'password': 'testpasswordWORD123',
        'password_confirm': 'testpasswordWORD123',
        'full_name': 'Test Tutor',
        'phone_number': '+375291234567',
        'specialization': 'Math',
    }
    response = client.post(reverse('register_tutor'), registration_data)
    if response.status_code != 302:
        print(response.context['form'].errors)
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
    assert response.url == reverse('profile-tutor')

@pytest.mark.django_db
def test_tutor_logout(client):
    tutor = Tutor.objects.create_user(
        email='testtutor@example.com',
        password='testpassword123',
        full_name='Test Tutor',
        phone_number='+375291234567',
        specialization='Math'
    )
    client.login(email='testtutor@example.com', password='testpassword123')
    response = client.post(reverse('logout-tutor'))
    assert response.status_code == 302
    assert not response.wsgi_request.user.is_authenticated
    assert response.url == reverse('main-page')


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