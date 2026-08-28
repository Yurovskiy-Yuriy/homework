from django.contrib import admin
from .models import Phone # Импортируем нашу модель

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    """Настройки отображения модели в админке"""

    list_display = ['name', 'price', 'lte_exists', 'description', 'image']  # Какие поля показывать в списке (можно добавить release_date, description и т.д.)
    search_fields = ['name']                        # Поиск по названию телефона
    list_filter = ['release_date', 'lte_exists']   # Фильтры: дата выхода и наличие LTE
