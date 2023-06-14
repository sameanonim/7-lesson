import os
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[self.id])
    
class Product(models.Model):
    id = models.AutoField(primary_key=True) # это поле будет автоматически увеличиваться при каждой новой записи
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image:
            ext = os.path.splitext(self.image.name)[1]
            self.image.name = f"{self.name}{ext}"
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return None
        
    def get_absolute_url(self):
        # Получаем URL-адрес для детального представления продукта
        return reverse('product_detail', args=[str(self.id)])
        
    @classmethod
    def get_active_version(cls, product_id):
        product = cls.objects.get(id=product_id)
        active_version = product.version_set.filter(is_active=True).first()
        return active_version
    
    class Meta:
        db_table = 'catalog_product'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    number_version = models.IntegerField()
    name_version = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name} - {self.name_version}'

    # метод для сохранения версии в базу данных с проверкой на уникальность активной версии
    def save(self, *args, **kwargs):
        # если эта версия активна
        if self.is_current:
            # то находим все другие активные версии для этого продукта и делаем их неактивными
            other_active_versions = Version.objects.filter(product=self.product, is_current=True).exclude(pk=self.pk)
            other_active_versions.update(is_current=False)
        # вызываем метод родительского класса для сохранения версии в базу данных
        super().save(*args, **kwargs)
    
# Создаем модель блоговой записи
class Post(models.Model):
    # Заголовок статьи
    title = models.CharField(max_length=200)
    # Slug url, который формируется из заголовка
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    # Содержимое статьи
    content = models.TextField()
    # Превью изображение
    preview = models.ImageField(upload_to='posts/')
    # Дата создания статьи
    created_at = models.DateTimeField(auto_now_add=True)
    # Признак публикации статьи
    published = models.BooleanField(default=False)
    # Количество просмотров статьи
    views = models.PositiveIntegerField(default=0)

    # Метод для получения абсолютного url статьи
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    # Метод для автоматического создания slug из заголовка
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # Метод для отображения названия статьи в админке
    def __str__(self):
        return self.title