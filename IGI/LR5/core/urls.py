from django.urls import path
from . import views

urlpatterns = [
    # Главная
    path('', views.HomeView.as_view(), name='home'),
    
    # Услуги (CRUD)
    path('services/', views.ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('services/add/', views.ServiceCreateView.as_view(), name='service-add'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service-edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service-delete'),
    
    # Заказы
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/add/', views.OrderCreateView.as_view(), name='order-add'),
    
    # Общие страницы
    path('news/', views.ArticleListView.as_view(), name='article-list'),
    path('glossary/', views.GlossaryListView.as_view(), name='glossary-list'),
    path('contacts/', views.ContactListView.as_view(), name='contact-list'),
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancy-list'),
    path('promocodes/', views.PromoCodeListView.as_view(), name='promocode-list'),
    path('about/', views.CompanyInfoView.as_view(), name='company-info'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    
    # Статистика
    path('stats/', views.StatsView.as_view(), name='stats'),
]