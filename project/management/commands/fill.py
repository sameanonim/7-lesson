from django.core.management import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Delete all objects
        Category.objects.all().delete() 		# Delete all categories (without deleting products)
        Product.objects.all().delete()		# Delete all products (without deleting categories)

        category1 = Category.objects.create(name='Ноутбуки', description='Категория ноутбуков')
        category2 = Category.objects.create(name='Планшеты', description='Категория планшетов')
        category3 = Category.objects.create(name='Смартфоны', description='Категория смартфонов')

        product1 = Product.objects.create(category=category1, name='Ноутбук Lenovo', description='Ноутбук Lenovo с процессором Intel Core i5, оперативной памятью8 ГБ и жестким диском256 ГБ', price=59990)
        product2 = Product.objects.create(category=category1, name='Ноутбук Asus', description='Ноутбук Asus с процессором Intel Core i7, оперативной памятью16 ГБ и жестким диском512 ГБ', price=79990)
        product3 = Product.objects.create(category=category2, name='Планшет Samsung', description='Планшет Samsung с экраном10 дюймов, оперативной памятью4 ГБ и встроенной памятью64 ГБ', price=19990)