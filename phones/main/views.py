from django.shortcuts import render, get_object_or_404
from .models import Phone

def catalog(request):
    phones = Phone.objects.all()
    return render(request, 'catalog.html', {'phones': phones})

def phone_detail(request, phone_id):
    phone = get_object_or_404(Phone, id=phone_id)
    return render(request, 'detail.html', {'phone': phone})