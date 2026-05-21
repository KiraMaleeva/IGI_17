from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r'^\+375 \(2[59]\) \d{3}-\d{2}-\d{2}$',
    message='Формат: +375 (29) XXX-XX-XX'
)


# ───── Справочники ─────

class ServiceType(models.Model):
    name = models.CharField('Тип услуги', max_length=100)

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'

    def __str__(self):
        return self.name


class CarType(models.Model):
    name = models.CharField('Тип авто', max_length=100)

    class Meta:
        verbose_name = 'Тип авто'
        verbose_name_plural = 'Типы авто'

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField('Специализация', max_length=100)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name


# ───── Основные сущности ─────

class Service(models.Model):
    name = models.CharField('Название', max_length=200)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)])
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,
                                     verbose_name='Тип')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'{self.name} ({self.price} руб.)'


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=20, validators=[phone_validator])
    birth_date = models.DateField('Дата рождения')
    specializations = models.ManyToManyField(Specialization,
                                             verbose_name='Специализации')

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=20, validators=[phone_validator])
    birth_date = models.DateField('Дата рождения')
    car_type = models.ForeignKey(CarType, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='Тип авто')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнен'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               verbose_name='Клиент')
    master = models.ForeignKey(Master, on_delete=models.CASCADE,
                               verbose_name='Мастер')
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    status = models.CharField('Статус', max_length=20,
                              choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk} — {self.client}'

    def total_price(self):
        return sum(s.price for s in self.services.all())


# ───── Общие страницы ─────

class Article(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    summary = models.CharField('Краткое содержание', max_length=300)
    content = models.TextField('Полный текст')
    image = models.ImageField('Картинка', upload_to='articles/', blank=True)
    published = models.DateTimeField('Опубликовано', auto_now_add=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published']

    def __str__(self):
        return self.title


class GlossaryEntry(models.Model):
    question = models.CharField('Вопрос/термин', max_length=300)
    answer = models.TextField('Ответ/определение')
    added_at = models.DateField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Термин'
        verbose_name_plural = 'Словарь терминов'

    def __str__(self):
        return self.question


class Contact(models.Model):
    name = models.CharField('Имя', max_length=100)
    role = models.CharField('Должность', max_length=200)
    phone = models.CharField('Телефон', max_length=20, validators=[phone_validator])
    email = models.EmailField('Email')
    photo = models.ImageField('Фото', upload_to='contacts/', blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name


class Review(models.Model):
    author_name = models.CharField('Имя', max_length=100)
    rating = models.IntegerField('Оценка', validators=[MinValueValidator(1)])
    text = models.TextField('Текст отзыва')
    date = models.DateField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.author_name} — {self.rating}★'


class Vacancy(models.Model):
    title = models.CharField('Должность', max_length=200)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title


class PromoCode(models.Model):
    code = models.CharField('Промокод', max_length=50, unique=True)
    discount = models.IntegerField('Скидка %', validators=[MinValueValidator(1)])
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return f'{self.code} — {self.discount}%'


class CompanyInfo(models.Model):
    text = models.TextField('Текст о компании')
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

    def __str__(self):
        return 'Информация о компании'