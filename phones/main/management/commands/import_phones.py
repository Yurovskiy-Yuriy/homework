import csv

from django.core.management.base import BaseCommand
from main.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r',  encoding='utf-8-sig') as file:
            phones = list(csv.DictReader(file, delimiter=',')) # ← либо 'точка с запятой' если в csv заголовки разделены 'точка с запятой'

        for phone_data in phones:
            
             # Преобразуем дату из формата DD.MM.YYYY в YYYY-MM-DD
            date_str = phone_data['release_date']
            if '.' in date_str:  # Если дата в формате DD.MM.YYYY
                day, month, year = date_str.split('.')
                formatted_date = f"{year}-{month}-{day}"
            else:
                formatted_date = date_str  # Если уже в правильном формате
            
            
            # Создаем объект Phone из данных CSV
            phone = Phone(
                id=int(phone_data['id']),
                name=phone_data['name'],
                price=int(phone_data['price']),
                image=phone_data['image'],
                release_date=formatted_date,  # Используем преобразованную дату
                lte_exists=phone_data['lte_exists'].lower() == 'true',
            )
            phone.save()
            self.stdout.write(self.style.SUCCESS(f'Добавлен телефон: {phone.name}'))