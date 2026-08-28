from django.db import models

class Phone(models.Model):
    # id создаётся автоматически
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.CharField(max_length=500, verbose_name='Ссылка на изображение')
    release_date = models.DateField(verbose_name='Дата выхода')
    lte_exists = models.BooleanField(default=False, verbose_name='Наличие LTE')
    description = models.TextField(verbose_name='Описание', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'