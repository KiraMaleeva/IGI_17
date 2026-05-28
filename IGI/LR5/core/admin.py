from django.contrib import admin
from .models import *


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(PartType)
class PartTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'part_type', 'quantity']
    list_filter = ['part_type']
    search_fields = ['name']
    

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'service_type']
    list_filter = ['service_type']
    search_fields = ['name']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date']
    filter_horizontal = ['specializations']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date', 'car_type']
    list_filter = ['car_type']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'master', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    filter_horizontal = ['services', 'parts']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published']
    search_fields = ['title', 'content']


@admin.register(GlossaryEntry)
class GlossaryEntryAdmin(admin.ModelAdmin):
    list_display = ['question', 'added_at']
    search_fields = ['question', 'answer']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'phone', 'email']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'rating', 'date']
    list_filter = ['rating', 'date']


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'is_active']
    list_filter = ['is_active']


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['updated_at']