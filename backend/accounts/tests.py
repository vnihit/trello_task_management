from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.
User = get_user_model()

class AccountsTest(APITestCase):

    def test_signup(self):
        """
        Ensure we can create new users.
        """
        url = "/accounts/local/"
        data = {"username": "test_user", "password": "test_password", "email": "abc@gmail.com"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_user')
        
    
