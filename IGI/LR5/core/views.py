from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q, Avg, Count
from django.utils import timezone
from django.core.paginator import Paginator
import calendar as cal
import requests
import statistics
import logging
from .models import *
from .forms import ServiceForm, OrderForm, ReviewForm

logger = logging.getLogger(__name__)


# ───── Главная ─────
def home(request):
    context = {
        'latest_article': Article.objects.first(),
        'services_count': Service.objects.count(),
        'orders_count': Order.objects.count(),
    }
    logger.info("Главная страница загружена")
    return render(request, 'core/home.html', context)


# ───── CRUD для Services (Function-Based) ─────
def service_list(request):
    services = Service.objects.all()
    
    # Поиск
    q = request.GET.get('q')
    if q:
        services = services.filter(Q(name__icontains=q) | Q(service_type__name__icontains=q))
        logger.debug(f"Поиск услуг по запросу: {q}")
    
    # Сортировка
    sort = request.GET.get('sort', 'name')
    if sort in ['name', 'price', '-price']:
        services = services.order_by(sort)
    
    # Пагинация
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/service_list.html', {'page_obj': page_obj, 'services': page_obj})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'core/service_detail.html', {'object': service})


@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            logger.info(f"Создана новая услуга: {service.name} пользователем {request.user}")
            return redirect('service-list')
    else:
        form = ServiceForm()
    return render(request, 'core/service_form.html', {'form': form})


@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            logger.info(f"Услуга обновлена: {service.name}")
            return redirect('service-list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'core/service_form.html', {'form': form, 'object': service})


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        logger.warning(f"Услуга удалена: {service.name}")
        service.delete()
        return redirect('service-list')
    return render(request, 'core/service_confirm_delete.html', {'object': service})


# ───── Заказы ─────
@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'core/order_list.html', {'orders': orders})


@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            logger.info(f"Создан новый заказ для клиента: {order.client}")
            return redirect('order-list')
    else:
        form = OrderForm()
    return render(request, 'core/order_form.html', {'form': form})


# ───── Общие страницы ─────
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'core/article_list.html', {'articles': articles})


def glossary_list(request):
    entries = GlossaryEntry.objects.all()
    return render(request, 'core/glossary_list.html', {'entries': entries})


def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'core/contact_list.html', {'contacts': contacts})


def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'core/review_list.html', {'reviews': reviews})


@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review-list')
    else:
        form = ReviewForm()
    return render(request, 'core/review_form.html', {'form': form})


def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'core/vacancy_list.html', {'vacancies': vacancies})


def promocode_list(request):
    promocodes = PromoCode.objects.all()
    return render(request, 'core/promocode_list.html', {'promocodes': promocodes})


def company_info(request):
    info = CompanyInfo.objects.first()
    return render(request, 'core/company_info.html', {'info': info})


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


# ───── Статистика ─────
@login_required
def stats_view(request):
    context = {}
    
    # Тайм-зона
    context['now_utc'] = timezone.now()
    context['now_local'] = timezone.localtime(timezone.now())
    context['calendar'] = cal.month(timezone.now().year, timezone.now().month)
    
    # Статистика
    context['total_orders'] = Order.objects.count()
    context['total_clients'] = Client.objects.count()
    
    # Цены услуг
    prices = list(Service.objects.values_list('price', flat=True))
    if prices:
        context['avg_price'] = statistics.mean(prices)
        context['median_price'] = statistics.median(prices)
    else:
        context['avg_price'] = 0
        context['median_price'] = 0
    
    # Популярные категории
    context['popular_types'] = ServiceType.objects.annotate(
        service_count=Count('service')
    ).order_by('-service_count')
    
    context['most_ordered_type'] = ServiceType.objects.annotate(
        order_count=Count('service__order')
    ).order_by('-order_count').first()
    
    # API погоды
    try:
        weather_url = 'https://wttr.in/Minsk?format=j1'
        weather_response = requests.get(weather_url, timeout=5)
        if weather_response.status_code == 200:
            data = weather_response.json()
            context['weather'] = {
                'temp': data['current_condition'][0]['temp_C'],
                'description': data['current_condition'][0]['weatherDesc'][0]['value']
            }
            logger.info("API погоды успешно загружен")
        else:
            context['weather'] = None
    except Exception as e:
        context['weather'] = None
        logger.error(f"Ошибка API погоды: {e}")
    
    # API валют
    try:
        currency_url = 'https://api.exchangerate-api.com/v4/latest/USD'
        currency_response = requests.get(currency_url, timeout=5)
        if currency_response.status_code == 200:
            context['currency'] = currency_response.json()
            logger.info("API курса валют успешно загружен")
        else:
            context['currency'] = None
    except Exception as e:
        context['currency'] = None
        logger.error(f"Ошибка API валют: {e}")
    
    # Генерация графика (Matplotlib вместо Chart.js)
    import matplotlib
    matplotlib.use('Agg')  # Без GUI
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
    
    # Данные для графика
    types = list(context['popular_types'])
    labels = [t.name for t in types]
    values = [t.service_count for t in types]
    
    # Создаём график
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('Тип услуги')
    plt.ylabel('Количество')
    plt.title('Популярные категории услуг')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Сохраняем в base64 для вставки в HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    context['chart'] = graphic
    
    return render(request, 'core/stats.html', context)


# ───── Регистрация ─────
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"Новый пользователь зарегистрирован: {user.username}")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})