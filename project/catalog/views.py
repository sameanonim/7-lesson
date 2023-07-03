from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from .models import Product, Post, Version
from .forms import ProductForm, VersionForm
from django.contrib import messages

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        version = product.версии.filter(is_current=True).first()
        context['version'] = version
        return context

class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    template_name = 'create_product.html'
    success_url = reverse_lazy('home')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('home')

    def get_success_url(self, *args, **kwargs):
        return reverse('update_product', args=[self.get_object().pk])
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    # Указываем модель, для которой создается форма
    model = Product
    # указываем шаблон
    template_name = 'delete_product.html'
    #у указываем адрес перенаправления
    success_url = reverse_lazy('home')

class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'version_form.html'
    success_url = '/'

class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'update_version.html'
    success_url = '/'

class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'version_confirm_delete.html'
    success_url = '/'

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