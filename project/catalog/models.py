from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Product( models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # метод для получения активной версии продукта, если она есть
    def get_active_version(self):
        # фильтруем версии по признаку текущей и берем первую из них
        active_version = self.version_set.filter(is_active=True).first()
        # возвращаем активную версию или None, если ее нет
        return active_version
    
class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='version_set')
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.number} - {self.name}"

    # метод для сохранения версии в базу данных с проверкой на уникальность активной версии
    def save(self, *args, **kwargs):
        # если эта версия активна
        if self.is_active:
            # то находим все другие активные версии для этого продукта и делаем их неактивными
            other_active_versions = Version.objects.filter(product=self.product, is_active=True).exclude(pk=self.pk)
            other_active_versions.update(is_active=False)
        # вызываем метод родительского класса для сохранения версии в базу данных
        super().save(*args, **kwargs)

class Meta:
    db_table = 'catalog_product'
    ordering = ['name']
    
    def __str__(self):
        return self.name
    
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