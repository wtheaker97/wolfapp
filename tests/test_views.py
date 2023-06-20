import pytest
from django.contrib.auth.models import User
from django.test import Client, RequestFactory
from django.urls import reverse
from personalprofile.models import Profile, Address
from personalprofile import forms, views

@pytest.fixture
def rf():
    return RequestFactory()

@pytest.fixture
def user():
    user = User.objects.create_user(username="test_user", password="password")
    return user

@pytest.fixture
def client(user):
    client = Client()
    client.force_login(user)
    return client

@pytest.fixture
def profile(user):
    profile = Profile.objects.create(
        user=user,
        name="Test User",
        phone_number="1234567890",
        date_of_birth="2000-01-01"
    )
    return profile

@pytest.fixture
def address(profile):
    address = Address.objects.create(
        profile=profile,
        address_1="1 Test Road",
        address_2="Test Village",
        city="Testville",
        postcode="T35T"
    )
    return address


@pytest.mark.django_db
def test_get_create_profile_user_without_profile(client):
    """Test a user without a profile can get the create_profile view"""
    response = client.get(reverse("create_profile"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_create_profile_user_with_profile(client, profile, address):
    """Test a user with a profile is redirected to the view_profile view"""
    response = client.get(reverse("create_profile"))
    assert response.status_code == 302
    assert response.url == reverse("view_profile")

@pytest.mark.django_db
def test_post_create_profile_valid_form(client):
    """Test a profile is created and the user is redirected when a valid form is submitted"""
    data = {
        "name": "Wolf",
        "phone_number": "12345678910",
        "date_of_birth": "2000-01-01",
        "address_1": "1 Test Road",
        "address_2": "Test Village",
        "city": "Testville",
        "postcode": "T35T"
    }
    response = client.post(reverse("create_profile"), data)
    assert response.status_code == 302
    assert response.url == reverse("view_profile")
    assert Profile.objects.count() == 1
    assert Profile.objects.get().name == "Wolf"

@pytest.mark.django_db
def test_post_create_profile_invalid_form(client):
    """Test an invalid form is not validated and the user is not redirected"""
    data = {
        "name": "Wolf",
        "phone_number": "12345678910",
        "date_of_birth": "3000-01-01",
        "address_1": "1 Test Road",
        "address_2": "Test Village",
        "city": "Testville",
        "postcode": "T35T"
    }
    profile_form = forms.ProfileForm(data)
    assert profile_form.is_valid() == False

    response = client.post(reverse("create_profile"), data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_view_profile_user_with_profile(client, profile, address):
    """Test a user with a profile can view their profile"""
    response = client.get(reverse("view_profile"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_view_profile_user_without_profile(client):
    """Test a user without a profile is redirected to the create_profile view"""
    response = client.get(reverse("view_profile"))
    assert response.status_code == 302
    assert response.url == reverse("create_profile")

@pytest.mark.django_db
def test_get_update_profile_user_with_profile(client, profile, address):
    """Test a user with a profile can get the update_profile view"""
    response = client.get(reverse("update_profile"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_update_profile_user_without_profile(client):
    """Test a user without a profile is redirected to the create_profile view"""
    response = client.get(reverse("update_profile"))
    assert response.status_code == 302
    assert response.url == reverse("create_profile")

@pytest.mark.django_db
def test_post_update_profile_same_address(client, profile, address):
    """Test updating a profile without changing the address updates the profile
    and the user is redirected to view_profile but doesn't create a new address.
    """
    new_data = {
        "name": "Badger",
        "phone_number": profile.phone_number,
        "date_of_birth": profile.date_of_birth,
        "address_1": address.address_1 ,
        "address_2": address.address_2,
        "city": address.city,
        "postcode": address.postcode
    }
    response = client.post(reverse("update_profile"), new_data)
    assert response.status_code == 302
    assert response.url == reverse("view_profile")
    assert Profile.objects.count() == 1
    assert Profile.objects.get().name == "Badger"
    assert Address.objects.count() == 1

@pytest.mark.django_db
def test_post_update_profile_new_address(client, profile, address):
    """Test updating a profile and address updates creates a new current address
    and redirects to view_profile.
    """
    new_data = {
        "name": profile.name,
        "phone_number": profile.phone_number,
        "date_of_birth": profile.date_of_birth,
        "address_1": "1 Wolf Road",
        "address_2": "Badger Town",
        "city": "London",
        "postcode": "W1A 1AA"
    }
    response = client.post(reverse("update_profile"), new_data)
    assert response.status_code == 302
    assert response.url == reverse("view_profile")
    assert Address.objects.count() == 2
    orig_addr = Address.objects.get(id=1)
    new_addr = Address.objects.get(id=2)
    assert new_addr.address_1 == new_data["address_1"]
    assert new_addr.current == True
    assert new_addr.profile == profile
    assert orig_addr.current == False

@pytest.mark.django_db
def test_post_update_profile_edited_address(client, profile, address):
    """Test slightly updating and address just updates the existing address
    without creating a new one.
    """
    new_data = {
        "name": profile.name,
        "phone_number": profile.phone_number,
        "date_of_birth": profile.date_of_birth,
        "address_1": "1 Wolf Road",
        "address_2": address.address_2,
        "city": address.city,
        "postcode": address.postcode
    }
    response = client.post(reverse("update_profile"), new_data)
    assert response.status_code == 302
    assert response.url == reverse("view_profile")
    assert Address.objects.count() == 1
    assert Address.objects.get().city == new_data["city"]
    assert Address.objects.get().current == True

@pytest.mark.django_db
def test_post_update_profile_invalid_form(client, profile, address):
    """Test an invalid form is not validated and the user is not redirected"""
    data = {
        "name": profile.name,
        "phone_number": profile.phone_number,
        "date_of_birth": "3000-01-01",
        "address_1": address.address_1,
        "address_2": address.address_2,
        "city": address.city,
        "postcode": address.postcode
    }
    profile_form = forms.ProfileForm(data)
    assert profile_form.is_valid() == False
    response = client.post(reverse("update_profile"), data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_profile(client, profile, address):
    """Test the delete_profile view will delete the profile and redirect to home"""
    assert Profile.objects.count() == 1
    assert Address.objects.count() == 1
    response = client.get(reverse("delete_profile"))
    assert Profile.objects.count() == 0
    assert Address.objects.count() == 0
    assert response.url == reverse("home")
