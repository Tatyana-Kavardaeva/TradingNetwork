from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from network.models import Company
from django.contrib.auth import get_user_model

User = get_user_model()


class CompanyTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='1234abcd')
        self.factory = Company.objects.create(name='Factory', email='factory@test.com', country='Россия', city='Москва',
                                              type='factory', company_level=0)
        self.retail = Company.objects.create(name='retail', email='retail@test.com', country='Россия', city='Москва',
                                             type='retail', company_level=1)
        self.individual = Company.objects.create(name='individual', email='individual@test.com', country='Россия',
                                                 city='Москва', type='individual', company_level=2)

    def test_create_company(self):
        """ Проверяет создание компании. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        data = {'name': 'Test New', 'email': 'factory1@test.com', 'country': 'Россия', 'city': 'Москва',
                'type': 'factory', 'company_level': 0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.all().count(), 4)

    def test_create_company_twin(self):
        """ Проверяет создание компании-двойника. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        data = {'name': 'Factory', 'email': 'factory2@test.com', 'country': 'Россия', 'city': 'Москва',
                'type': 'factory', 'company_level': 0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Компания уже существует в этом регионе.']})

    def test_create_company_with_email(self):
        """ Проверяет создание компании c одинаковыми email-адресами. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        data = {'name': 'Test New', 'email': 'factory@test.com', 'country': 'Россия', 'city': 'Москва',
                'type': 'factory', 'company_level': 0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['Такой email уже зарегистрирован.']})

    def test_create_factory_with_supplier(self):
        """ Проверяет создание завода c поставщиком. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        data = {'name': 'Test New', 'email': 'factory4@test.com', 'country': 'Россия', 'city': 'Москва',
                'type': 'factory', 'company_level': 0, 'supplier': self.retail.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Завод не может иметь поставщика.']})

    def test_create_retail_with_supplier(self):
        """ Проверяет создание розничной сети c поставщиком ИП. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        data = {'name': 'Test', 'email': 'retail1@test.com', 'country': 'Россия', 'city': 'Москва',
                'type': 'retail', 'supplier': self.individual.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['ИП не может быть поставщиком для розницы.']})

    def test_create_retail_without_supplier(self):
        """ Проверяет создание розничной сети без поставщика. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        data = {'name': 'Test', 'email': 'retail1@test.com', 'country': 'Россия', 'city': 'Москва',
                'type': 'retail'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Выберите поставщика.']})

    def test_create_individual_without_supplier(self):
        """ Проверяет создание ИП без поставщика. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        data = {'name': 'Test', 'email': 'individual1@test.com', 'country': 'Россия', 'city': 'Москва',
                'type': 'individual'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Выберите поставщика.']})

    def test_create_company_with_supplier(self):
        """ Проверяет создание компании c поставщиком, имеющим второй уровень иерархии. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        data = {'name': 'Test', 'email': 'company@test.com', 'country': 'Россия', 'city': 'Москва',
                'type': 'individual', 'supplier': self.individual.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Компания с уровнем 2 не может быть поставщиком.']}
        )

    def test_retrieve_company(self):
        """ Проверяет просмотр информации о компании. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-detail', args={self.factory.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Factory')

    def test_update_company(self):
        """ Проверяет обновление компании. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-detail', args=(self.factory.pk,))
        data = {'name': 'Factory update', 'type': 'factory'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Factory update')

    def test_update_debt_company(self):
        """ Проверяет обновление поля 'задолженность перед поставщиком'. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-detail', args=(self.factory.pk,))
        data = {'name': 'Factory update', 'type': 'factory', 'debt': '1.00'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('debt'), '0.00')

    def test_delete_company(self):
        """ Проверяет удаление компании. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-detail', args=(self.factory.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.all().count(), 2)

    def test_list_company(self):
        """ Проверяет просмотр списка компаний. """

        self.client.force_authenticate(user=self.user)
        url = reverse('network:company-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
