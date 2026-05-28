from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q, Avg, Count, Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.core.paginator import Paginator
from decimal import Decimal
import calendar as cal
import requests
import statistics
import logging
from .models import *
from .forms import ServiceForm, PartForm, OrderAdminForm, OrderClientForm, ReviewForm

logger = logging.getLogger(__name__)


# ───── Проверка ролей ─────

def is_master(user):
    return hasattr(user, 'master')


def is_client(user):
    return hasattr(user, 'client')


# ───── Главная ─────
def home(request):
    context = {
        'latest_article': Article.objects.first(),
        'services_count': Service.objects.count(),
        'orders_count': Order.objects.count(),
    }
    logger.info("Главная страница загружена")
    return render(request, 'core/home.html', context)


# ───── CRUD для Запчастей ─────

@login_required
@user_passes_test(lambda u: u.is_superuser)
def part_list(request):
    parts = Part.objects.all()
    
    # Поиск
    q = request.GET.get('q')
    if q:
        parts = parts.filter(Q(name__icontains=q) | Q(part_type__name__icontains=q))
    
    # Фильтрация по типу
    part_type_id = request.GET.get('type')
    if part_type_id:
        parts = parts.filter(part_type_id=part_type_id)
    
    # Сортировка
    sort = request.GET.get('sort', 'name')
    if sort in ['name', 'price', '-price', 'quantity', '-quantity']:
        parts = parts.order_by(sort)
    
    # Пагинация
    paginator = Paginator(parts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    part_types = PartType.objects.all()
    
    return render(request, 'core/part_list.html', {
        'page_obj': page_obj,
        'parts': page_obj,
        'part_types': part_types
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def part_create(request):
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            part = form.save()
            logger.info(f"Создана новая запчасть: {part.name}")
            return redirect('part-list')
    else:
        form = PartForm()
    return render(request, 'core/part_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def part_update(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            logger.info(f"Запчасть обновлена: {part.name}")
            return redirect('part-list')
    else:
        form = PartForm(instance=part)
    return render(request, 'core/part_form.html', {'form': form, 'object': part})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def part_delete(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        logger.warning(f"Запчасть удалена: {part.name}")
        part.delete()
        return redirect('part-list')
    return render(request, 'core/part_confirm_delete.html', {'object': part})


# ───── CRUD для Services ─────

def service_list(request):
    services = Service.objects.all()
    
    # Поиск
    q = request.GET.get('q')
    if q:
        services = services.filter(Q(name__icontains=q) | Q(service_type__name__icontains=q))
        logger.debug(f"Поиск услуг по запросу: {q}")
    
    # Фильтрация по типу
    service_type_id = request.GET.get('type')
    if service_type_id:
        services = services.filter(service_type_id=service_type_id)
    
    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        services = services.filter(price__gte=min_price)
    if max_price:
        services = services.filter(price__lte=max_price)
    
    # Сортировка
    sort = request.GET.get('sort', 'name')
    if sort in ['name', 'price', '-price']:
        services = services.order_by(sort)
    
    # Пагинация
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Передаём типы услуг для фильтра
    service_types = ServiceType.objects.all()
    
    return render(request, 'core/service_list.html', {
        'page_obj': page_obj,
        'services': page_obj,
        'service_types': service_types
    })


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'core/service_detail.html', {'object': service})


@login_required
@user_passes_test(lambda u: u.is_superuser)
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
@user_passes_test(lambda u: u.is_superuser)
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
@user_passes_test(lambda u: u.is_superuser)
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
    if request.user.is_superuser:
        orders = Order.objects.all()
    elif is_master(request.user):
        orders = Order.objects.filter(master=request.user.master)
    elif is_client(request.user):
        orders = Order.objects.filter(client=request.user.client)
    else:
        orders = Order.objects.none()
    
    return render(request, 'core/order_list.html', {'orders': orders})


@login_required
def order_create(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = OrderAdminForm(request.POST)
        elif is_client(request.user):
            form = OrderClientForm(request.POST)
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("У вас нет прав для создания заказа")
        
        if form.is_valid():
            order = form.save(commit=False)
            
            if is_client(request.user):
                order.client = request.user.client
                order.status = 'new'
            
            order.save()
            form.save_m2m()
            
            logger.info(f"Создан новый заказ #{order.id} для клиента: {order.client}")
            return redirect('order-list')
    else:
        if request.user.is_superuser:
            form = OrderAdminForm()
        elif is_client(request.user):
            form = OrderClientForm()
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("У вас нет прав для создания заказа")
    
    return render(request, 'core/order_form.html', {'form': form})


# ───── Личный кабинет мастера ─────

@login_required
@user_passes_test(is_master)
def master_dashboard(request):
    master = request.user.master
    orders = Order.objects.filter(master=master).select_related('client')
    
    context = {
        'master': master,
        'orders': orders,
        'orders_new': orders.filter(status='new').count(),
        'orders_in_progress': orders.filter(status='in_progress').count(),
        'orders_done': orders.filter(status='done').count(),
    }
    return render(request, 'core/master_dashboard.html', context)


# ───── Личный кабинет клиента ─────

@login_required
@user_passes_test(is_client)
def client_dashboard(request):
    client = request.user.client
    orders = Order.objects.filter(client=client).prefetch_related('services', 'parts').order_by('-created_at')
    
    context = {
        'client': client,
        'orders': orders,
    }
    return render(request, 'core/client_dashboard.html', context)


# ───── Общие страницы ─────

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'core/article_list.html', {'articles': articles})


def glossary_list(request):
    entries = GlossaryEntry.objects.all()
    return render(request, 'core/glossary_list.html', {'entries': entries})


def contact_list(request):
    contacts = Contact.objects.all()
    masters = Master.objects.select_related('user').all()
    context = {
        'contacts': contacts,
        'masters': masters,
    }
    return render(request, 'core/contact_list.html', context)


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
    """Промокоды (доступно всем)"""
    promocodes = PromoCode.objects.filter(is_active=True)
    return render(request, 'core/promocode_list.html', {'promocodes': promocodes})


def company_info(request):
    info = CompanyInfo.objects.first()
    return render(request, 'core/company_info.html', {'info': info})


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


# ───── Статистика (только admin) ─────

@login_required
@user_passes_test(lambda u: u.is_superuser)
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
    
    # Статистика по клиентам
    clients_with_orders = Client.objects.annotate(
        services_total=Coalesce(
            Sum('order__services__price'), 
            Value(0, output_field=DecimalField())
        ),
        parts_total=Coalesce(
            Sum('order__parts__price'), 
            Value(0, output_field=DecimalField())
        )
    ).annotate(
        total_spent=F('services_total') + F('parts_total')
    ).filter(total_spent__gt=0).order_by('-total_spent')
    
    context['clients_stats'] = clients_with_orders

    # Статистика по запчастям
    part_types_stats = PartType.objects.annotate(
        part_count=Count('part'),
        total_quantity=Coalesce(Sum('part__quantity'), 0)
    ).order_by('-part_count')
    context['part_types_stats'] = part_types_stats
    
    # API погоды
    try:
        weather_url = 'https://wttr.in/Minsk?format=j1'
        weather_response = requests.get(weather_url, timeout=5)
    
        if weather_response.status_code == 200:
            data = weather_response.json()
        
            if 'current_condition' in data and len(data['current_condition']) > 0:
                current = data['current_condition'][0]
                context['weather'] = {
                    'temp': current.get('temp_C', 'N/A'),
                    'description': current['weatherDesc'][0]['value'] if 'weatherDesc' in current else 'N/A'
                }
                logger.info("API погоды успешно загружен")
            else:
                context['weather'] = None
                logger.warning("API погоды вернуло некорректную структуру данных")
        else:
            context['weather'] = None
            logger.warning(f"API погоды вернуло статус {weather_response.status_code}")
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
    
    # График
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
    
    types = list(context['popular_types'])
    labels = [t.name for t in types]
    values = [t.service_count for t in types]
    
    if labels:
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel('Тип услуги')
        plt.ylabel('Количество')
        plt.title('Популярные категории услуг')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        graphic = base64.b64encode(image_png).decode('utf-8')
        context['chart'] = graphic
    else:
        context['chart'] = None
    
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