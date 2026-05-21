from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
import calendar as cal
import requests
from .models import *


# ───── Главная страница ─────
class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['latest_article'] = Article.objects.first()  # последняя статья
        ctx['services_count'] = Service.objects.count()
        ctx['orders_count'] = Order.objects.count()
        return ctx


# ───── Услуги (CRUD) ─────
class ServiceListView(ListView):
    model = Service
    template_name = 'core/service_list.html'
    context_object_name = 'services'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        # Поиск
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(service_type__name__icontains=q))
        # Сортировка
        sort = self.request.GET.get('sort', 'name')
        if sort in ['name', 'price', '-price']:
            qs = qs.order_by(sort)
        return qs


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'core/service_detail.html'


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    fields = ['name', 'price', 'service_type']
    template_name = 'core/service_form.html'
    success_url = reverse_lazy('service-list')


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ['name', 'price', 'service_type']
    template_name = 'core/service_form.html'
    success_url = reverse_lazy('service-list')


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'core/service_confirm_delete.html'
    success_url = reverse_lazy('service-list')


# ───── Заказы ─────
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/order_list.html'
    context_object_name = 'orders'


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['client', 'master', 'services', 'status']
    template_name = 'core/order_form.html'
    success_url = reverse_lazy('order-list')


# ───── Общие страницы ─────
class ArticleListView(ListView):
    model = Article
    template_name = 'core/article_list.html'
    context_object_name = 'articles'


class GlossaryListView(ListView):
    model = GlossaryEntry
    template_name = 'core/glossary_list.html'
    context_object_name = 'entries'


class ContactListView(ListView):
    model = Contact
    template_name = 'core/contact_list.html'
    context_object_name = 'contacts'


class ReviewListView(ListView):
    model = Review
    template_name = 'core/review_list.html'
    context_object_name = 'reviews'


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'core/vacancy_list.html'
    context_object_name = 'vacancies'


class PromoCodeListView(ListView):
    model = PromoCode
    template_name = 'core/promocode_list.html'
    context_object_name = 'promocodes'


class CompanyInfoView(TemplateView):
    template_name = 'core/company_info.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['info'] = CompanyInfo.objects.first()
        return ctx


class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy_policy.html'


# ───── Статистика + Тайм-зона + API ─────
class StatsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/stats.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        # Тайм-зона
        ctx['now_utc'] = timezone.now()
        ctx['now_local'] = timezone.localtime(timezone.now())
        ctx['calendar'] = cal.month(timezone.now().year, timezone.now().month)
        
        # Статистика
        ctx['total_orders'] = Order.objects.count()
        ctx['total_clients'] = Client.objects.count()
        ctx['avg_price'] = Service.objects.aggregate(Avg('price'))['price__avg']
        
        # Популярные категории
        ctx['popular_types'] = ServiceType.objects.annotate(
            service_count=Count('service')
        ).order_by('-service_count')
        
        # API 1: Погода (OpenWeatherMap)
        try:
            weather_key = 'YOUR_API_KEY'  # замени на свой ключ
            weather_url = f'https://api.openweathermap.org/data/2.5/weather?q=Minsk&appid={weather_key}&units=metric&lang=ru'
            weather_response = requests.get(weather_url, timeout=5)
            ctx['weather'] = weather_response.json() if weather_response.status_code == 200 else None
        except:
            ctx['weather'] = None
        
        # API 2: Курс валют
        try:
            currency_url = 'https://api.exchangerate-api.com/v4/latest/USD'
            currency_response = requests.get(currency_url, timeout=5)
            ctx['currency'] = currency_response.json() if currency_response.status_code == 200 else None
        except:
            ctx['currency'] = None
        
        return ctx