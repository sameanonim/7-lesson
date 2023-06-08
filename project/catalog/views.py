from django.urls import reverse_lazy
from django.db import models
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Post
from .forms import ProductForm

# Create your views here.

class HomeView(ListView):
    # Указываем модель, из которой берутся данные
    model = Product
    # Указываем имя шаблона для отображения списка товаров
    template_name = 'home.html'
    # Указываем имя переменной в контексте для списка товаров
    context_object_name = 'products'

class ContactsView(TemplateView):
    # Указываем имя шаблона для отображения контактов
    template_name = 'contacts.html'
    # Здесь вы можете добавить логику для получения контекста

class ProductDetailView(DetailView):
    # Указываем модель, из которой берутся данные
    model = Product
    # Указываем имя шаблона для отображения деталей товара
    template_name = 'product.html'
    # Указываем имя переменной в контексте для объекта товара
    context_object_name = 'product'
    # Указываем параметр, по которому ищется объект в базе данных
    pk_url_kwarg = 'product_id'

class CreateProductView(CreateView):
    # Указываем модель, для которой создается форма
    model = Product
    # Указываем форму, которая используется для создания объекта
    form_class = ProductForm
    # Указываем имя шаблона для отображения формы
    template_name = 'create_products.html'
    # Указываем URL, на который будет перенаправлен пользователь после успешного создания объекта
    success_url = reverse_lazy('product_list')

# Контроллер для отображения списка статей
class PostListView(ListView):
    # Указываем модель, из которой берутся данные
    model = Post
    # Указываем имя шаблона для отображения списка статей
    template_name = 'post_list.html'
    # Указываем имя переменной в контексте для списка статей
    context_object_name = 'posts'
    # Переопределяем метод get_queryset, чтобы фильтровать статьи по признаку публикации
    def get_queryset(self):
        return Post.objects.filter(published=True)

# Контроллер для отображения деталей статьи
class PostDetailView(DetailView):
    # Указываем модель, из которой берутся данные
    model = Post
    # Указываем имя шаблона для отображения деталей статьи
    template_name = 'post_detail.html'
    # Указываем имя переменной в контексте для объекта статьи
    context_object_name = 'post'
    # Указываем параметр, по которому ищется объект в базе данных
    slug_url_kwarg = 'slug'
    # Переопределяем метод get_object, чтобы увеличивать счетчик просмотров при открытии статьи
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj

# Контроллер для создания статьи
class PostCreateView(CreateView):
    # Указываем модель, для которой создается форма
    model = Post
    # Указываем поля, которые будут в форме
    fields = ['title', 'content', 'preview', 'published']
    # Указываем имя шаблона для отображения формы
    template_name = 'post_create.html'
    # Указываем URL, на который будет перенаправлен пользователь после успешного создания объекта
    success_url = reverse_lazy('post_list')

# Контроллер для редактирования статьи
class PostUpdateView(UpdateView):
    # Указываем модель, для которой создается форма
    model = Post
    # Указываем поля, которые будут в форме
    fields = ['title', 'content', 'preview', 'published']
    # Указываем имя шаблона для отображения формы
    template_name = 'post_update.html'
    # Указываем параметр, по которому ищется объект в базе данных
    slug_url_kwarg = 'slug'
    # Переопределяем метод get_success_url, чтобы перенаправлять пользователя на просмотр редактированной статьи
    def get_success_url(self):
        return self.object.get_absolute_url()

# Контроллер для удаления статьи
class PostDeleteView(DeleteView):
    # Указываем модель, из которой удаляется объект
    model = Post
    # Указываем имя шаблона для подтверждения удаления
    template_name = 'post_delete.html'
    # Указываем параметр, по которому ищется объект в базе данных
    slug_url_kwarg = 'slug'
    # Указываем URL, на который будет перенаправлен пользователь после успешного удаления объекта
    success_url = reverse_lazy('post_list')