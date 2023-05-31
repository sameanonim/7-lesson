from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm

# Create your views here.

def home(request):
    # Получаем список всех товаров из базы данных
    products = Product.objects.all()
    # Создаем словарь с переменной products для шаблона
    context = {'products': products}
    # Возвращаем отрендеренный шаблон home.html с контекстом
    # Убираем лишние фигурные скобки вокруг context
    return render(request, 'home.html', context)

def contacts(request):
    # здесь вы можете добавить логику для получения контекста
    context = {}
    return render(request, 'contacts.html', context)

def product_detail(request, product_id):
    # Получаем объект товара по его pk или возвращаем 404 ошибку, если он не найден
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    # Рендерим шаблон product.html с контекстом, содержащим объект product
    return render(request, 'product.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'create_products.html', {'form': form})
