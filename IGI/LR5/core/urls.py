from django.urls import path
from . import views

urlpatterns = [
    # Главная
    path('', views.home, name='home'),
    
    # Регистрация
    path('register/', views.register, name='register'),
    
    # Services CRUD
    path('services/', views.service_list, name='service-list'),
    path('services/<int:pk>/', views.service_detail, name='service-detail'),
    path('services/add/', views.service_create, name='service-add'),
    path('services/<int:pk>/edit/', views.service_update, name='service-edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service-delete'),
    
    # Orders
    path('orders/', views.order_list, name='order-list'),
    path('orders/add/', views.order_create, name='order-add'),
    
    # Общие страницы
    path('news/', views.article_list, name='article-list'),
    path('glossary/', views.glossary_list, name='glossary-list'),
    path('contacts/', views.contact_list, name='contact-list'),
    path('reviews/', views.review_list, name='review-list'),
    path('reviews/add/', views.review_create, name='review-add'),
    path('vacancies/', views.vacancy_list, name='vacancy-list'),
    path('promocodes/', views.promocode_list, name='promocode-list'),
    path('about/', views.company_info, name='company-info'),
    path('privacy/', views.privacy_policy, name='privacy-policy'),
    
    # Статистика
    path('stats/', views.stats_view, name='stats'),
]