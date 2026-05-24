from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from .models import *


class ServiceModelTest(TestCase):
    """Тесты модели Service"""
    
    def setUp(self):
        self.service_type = ServiceType.objects.create(name='Диагностика')
        self.service = Service.objects.create(
            name='Компьютерная диагностика',
            price=50,
            service_type=self.service_type
        )
    
    def test_service_creation(self):
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(self.service.name, 'Компьютерная диагностика')
    
    def test_service_price(self):
        self.assertEqual(self.service.price, 50)
    
    def test_service_str(self):
        self.assertIn('Компьютерная диагностика', str(self.service))


class OrderModelTest(TestCase):
    """Тесты модели Order"""
    
    def setUp(self):
        # Создаём пользователей
        self.user_client = User.objects.create_user('client1', password='pass')
        self.user_master = User.objects.create_user('master1', password='pass')
        
        # Создаём клиента и мастера
        self.car_type = CarType.objects.create(name='Легковой')
        self.client = Client.objects.create(
            user=self.user_client,
            phone='+375 (29) 111-11-11',
            birth_date=date(1990, 1, 1),
            car_type=self.car_type
        )
        
        self.specialization = Specialization.objects.create(name='Механик')
        self.master = Master.objects.create(
            user=self.user_master,
            phone='+375 (29) 222-22-22',
            birth_date=date(1985, 5, 15)
        )
        self.master.specializations.add(self.specialization)
        
        # Создаём услугу
        self.service_type = ServiceType.objects.create(name='Ремонт')
        self.service = Service.objects.create(
            name='Замена масла',
            price=30,
            service_type=self.service_type
        )
        
        # Создаём заказ
        self.order = Order.objects.create(
            client=self.client,
            master=self.master,
            status='new'
        )
        self.order.services.add(self.service)
    
    def test_order_creation(self):
        self.assertEqual(Order.objects.count(), 1)
    
    def test_order_total_price(self):
        self.assertEqual(self.order.total_price(), 30)
    
    def test_order_multiple_services(self):
        service2 = Service.objects.create(
            name='Диагностика',
            price=50,
            service_type=self.service_type
        )
        self.order.services.add(service2)
        self.assertEqual(self.order.total_price(), 80)


class ViewsTest(TestCase):
    """Тесты views"""
    
    def setUp(self):
        self.test_client = self.client  # сохраняем тестовый клиент Django
        self.user = User.objects.create_user('testuser', password='testpass')
        
        self.service_type = ServiceType.objects.create(name='Диагностика')
        self.service = Service.objects.create(
            name='Тестовая услуга',
            price=100,
            service_type=self.service_type
        )
    
    def test_home_page(self):
        response = self.test_client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Автосервис')
    
    def test_service_list(self):
        response = self.test_client.get(reverse('service-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая услуга')
    
    def test_service_detail(self):
        response = self.test_client.get(reverse('service-detail', args=[self.service.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая услуга')
    
    def test_service_create_requires_login(self):
        response = self.test_client.get(reverse('service-add'))
        self.assertEqual(response.status_code, 302)  # редирект на логин
    
    def test_service_create_authenticated(self):
        self.test_client.login(username='testuser', password='testpass')
        response = self.test_client.get(reverse('service-add'))
        self.assertEqual(response.status_code, 200)
    
    def test_service_search(self):
        response = self.test_client.get(reverse('service-list') + '?q=Тестовая')
        self.assertContains(response, 'Тестовая услуга')
    
    def test_service_sort(self):
        Service.objects.create(name='Другая услуга', price=200, service_type=self.service_type)
        response = self.test_client.get(reverse('service-list') + '?sort=-price')
        self.assertEqual(response.status_code, 200)


class ArticleModelTest(TestCase):
    """Тесты модели Article"""
    
    def setUp(self):
        self.article = Article.objects.create(
            title='Тестовая статья',
            summary='Краткое описание',
            content='Полный текст статьи'
        )
    
    def test_article_creation(self):
        self.assertEqual(Article.objects.count(), 1)
    
    def test_article_str(self):
        self.assertEqual(str(self.article), 'Тестовая статья')


class PromoCodeModelTest(TestCase):
    """Тесты модели PromoCode"""
    
    def setUp(self):
        self.promo = PromoCode.objects.create(
            code='TEST20',
            discount=20,
            is_active=True
        )
    
    def test_promocode_creation(self):
        self.assertEqual(PromoCode.objects.count(), 1)
    
    def test_promocode_discount(self):
        self.assertEqual(self.promo.discount, 20)
    
    def test_promocode_is_active(self):
        self.assertTrue(self.promo.is_active)


class ClientModelTest(TestCase):
    """Тесты модели Client"""
    
    def setUp(self):
        self.user = User.objects.create_user('testclient', password='pass')
        self.car_type = CarType.objects.create(name='Внедорожник')
        self.client_obj = Client.objects.create(
            user=self.user,
            phone='+375 (29) 123-45-67',
            birth_date=date(1992, 3, 15),
            car_type=self.car_type
        )
    
    def test_client_creation(self):
        self.assertEqual(Client.objects.count(), 1)
    
    def test_client_phone_format(self):
        self.assertIn('+375', self.client_obj.phone)


class MasterModelTest(TestCase):
    """Тесты модели Master"""
    
    def setUp(self):
        self.user = User.objects.create_user('testmaster', password='pass')
        self.spec = Specialization.objects.create(name='Диагност')
        self.master = Master.objects.create(
            user=self.user,
            phone='+375 (29) 987-65-43',
            birth_date=date(1985, 7, 20)
        )
        self.master.specializations.add(self.spec)
    
    def test_master_creation(self):
        self.assertEqual(Master.objects.count(), 1)
    
    def test_master_specializations(self):
        self.assertEqual(self.master.specializations.count(), 1)


class URLTest(TestCase):
    """Тесты доступности URL"""
    
    def setUp(self):
        self.test_client = self.client
    
    def test_home_url(self):
        response = self.test_client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_services_url(self):
        response = self.test_client.get('/services/')
        self.assertEqual(response.status_code, 200)
    
    def test_news_url(self):
        response = self.test_client.get('/news/')
        self.assertEqual(response.status_code, 200)
    
    def test_contacts_url(self):
        response = self.test_client.get('/contacts/')
        self.assertEqual(response.status_code, 200)