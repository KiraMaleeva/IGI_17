from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
import calendar as cal
import requests
import statistics
import logging
from .models import *

logger = logging.getLogger(__name__)


# ───── Главная страница ─────
class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['latest_article'] = Article.objects.first()  # последняя статья
        ctx['services_count'] = Service.objects.count()
        ctx['orders_count'] = Order.objects.count()
        logger.info("Главная страница загружена")
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
            logger.debug(f"Поиск услуг по запросу: {q}")
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
    
    def form_valid(self, form):
        logger.info(f"Создана новая услуга: {form.cleaned_data['name']} пользователем {self.request.user}")
        return super().form_valid(form)


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ['name', 'price', 'service_type']
    template_name = 'core/service_form.html'
    success_url = reverse_lazy('service-list')
    
    def form_valid(self, form):
        logger.info(f"Услуга обновлена: {form.cleaned_data['name']}")
        return super().form_valid(form)


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'core/service_confirm_delete.html'
    success_url = reverse_lazy('service-list')
    
    def delete(self, request, *args, **kwargs):
        logger.warning(f"Услуга удалена: {self.get_object().name}")
        return super().delete(request, *args, **kwargs)


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
    
    def form_valid(self, form):
        logger.info(f"Создан новый заказ для клиента: {form.cleaned_data['client']}")
        return super().form_valid(form)


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
        
        # Статистика по заказам и клиентам
        ctx['total_orders'] = Order.objects.count()
        ctx['total_clients'] = Client.objects.count()
        
        # Статистика по ценам (среднее и медиана)
        prices = list(Service.objects.values_list('price', flat=True))
        if prices:
            ctx['avg_price'] = statistics.mean(prices)
            ctx['median_price'] = statistics.median(prices)
        else:
            ctx['avg_price'] = 0
            ctx['median_price'] = 0
        
        # Популярные категории услуг (по количеству услуг)
        ctx['popular_types'] = ServiceType.objects.annotate(
            service_count=Count('service')
        ).order_by('-service_count')
        
        # Самый популярный тип услуг (по количеству в заказах)
        ctx['most_ordered_type'] = ServiceType.objects.annotate(
            order_count=Count('service__order')
        ).order_by('-order_count').first()
        
        # API 1: Погода (OpenWeatherMap)
        try:
            weather_key = 'd45459e22cce12864954d7a17e0619ff'
            weather_url = f'https://api.openweathermap.org/data/2.5/weather?q=Minsk&appid={weather_key}&units=metric&lang=ru'
            weather_response = requests.get(weather_url, timeout=5)
            if weather_response.status_code == 200:
                ctx['weather'] = weather_response.json()
                logger.info("API погоды успешно загружен")
            else:
                ctx['weather'] = None
                logger.warning(f"API погоды вернул код: {weather_response.status_code}")
        except Exception as e:
            ctx['weather'] = None
            logger.error(f"Ошибка загрузки API погоды: {e}")
        
        # API 2: Курс валют
        try:
            currency_url = 'https://api.exchangerate-api.com/v4/latest/USD'
            currency_response = requests.get(currency_url, timeout=5)
            if currency_response.status_code == 200:
                ctx['currency'] = currency_response.json()
                logger.info("API курса валют успешно загружен")
            else:
                ctx['currency'] = None
                logger.warning(f"API валют вернул код: {currency_response.status_code}")
        except Exception as e:
            ctx['currency'] = None
            logger.error(f"Ошибка загрузки API валют: {e}")
        
        return ctx