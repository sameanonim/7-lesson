from django.core.management import BaseCommand
from catalog.models import Category, Product, Post
from django.utils import timezone

class Command(BaseCommand):
    help = 'Внесение данных в Базу Данных'

    def handle(self, *args, **options):
        # Delete all objects
        Category.objects.all().delete() # Delete all categories
        Product.objects.all().delete() # Delete all products
        Post.objects.all().delete() # Delete all posts

        # Create categories
        category1 = Category.objects.create(name='Ноутбуки', description='Категория ноутбуков')
        category2 = Category.objects.create(name='Планшеты', description='Категория планшетов')
        category3 = Category.objects.create(name='Смартфоны', description='Категория смартфонов')

        # Create products
        product1 = Product.objects.create(category=category1, name='Ноутбук Lenovo', description='Ноутбук Lenovo с процессором Intel Core i5, оперативной памятью 8 ГБ и жестким диском 256 ГБ', price=59990.0, image='lenovo.jpg', created=timezone.now(), updated=timezone.now())
        product2 = Product.objects.create(category=category1, name='Ноутбук Asus', description='Ноутбук Asus с процессором Intel Core i7, оперативной памятью 16 ГБ и жестким диском 512 ГБ', price=79990.0, image='asus.jpg', created=timezone.now(), updated=timezone.now())
        product3 = Product.objects.create(category=category2, name='Планшет Samsung', description='Планшет Samsung с экраном 10 дюймов, оперативной памятью 4 ГБ и встроенной памятью 64 ГБ', price=19990.0, image='samsung.jpg', created=timezone.now(), updated=timezone.now())
        product4 = Product.objects.create(category=category2, name='Планшет Apple', description='Планшет Apple с экраном 11 дюймов, оперативной памятью 6 ГБ и встроенной памятью 128 ГБ', price=49990.0, image='apple.jpg', created=timezone.now(), updated=timezone.now())
        product5 = Product.objects.create(category=category3, name='Смартфон Xiaomi', description='Смартфон Xiaomi с экраном 6.5 дюймов, оперативной памятью 8 ГБ и встроенной памятью 128 ГБ', price=14990.0, image='xiaomi.jpg', created=timezone.now(), updated=timezone.now())

        # Create post
        post1 = Post.objects.create(id=2, title="Who When What Why", slug="whowhenwhywhat", content="About Walter Kronkait", preview="posts/qrcode.png", created_at="2023-06-08 21:31:49.956494+03", published=True, views=1) # Создаем объект Post с данными из задания
        post1.save() 