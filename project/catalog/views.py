from django.urls import reverse_lazy
from django import forms
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from .models import Product, Post
from .forms import ProductForm, VersionFormSet

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


class ProductCreateView(CreateView):
    # Указываем модель, для которой создается форма
    model = Product
    # Указываем форму, которая используется для создания объекта
    form_class = ProductForm
    # указываем шаблон
    template_name = 'create_product.html'
    #у указываем адрес перенаправления
    success_url = '/'

class ProductUpdateView(UpdateView):
    # Указываем модель, для которой создается форма
    model = Product
    # Указываем форму, которая используется для создания объекта
    form_class = ProductForm
    # указываем шаблон
    template_name = 'update_product.html'
    #у указываем адрес перенаправления
    success_url = '/'

        # метод для добавления дополнительного контекста в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # если запрос типа POST, то создаем формсет из полученных данных и файлов
        if self.request.POST:
            context['version_formset'] = VersionFormSet(self.request.POST, self.request.FILES, instance=self.object)
        # иначе создаем пустой формсет
        else:
            context['version_formset'] = VersionFormSet(instance=self.object)
        return context

    # метод для сохранения формы и формсета в базу данных
    def form_valid(self, form):
        context = self.get_context_data()
        version_formset = context['version_formset']
        # если формсет валиден, то сохраняем его вместе с формой
        if version_formset.is_valid():
            self.object = form.save()
            version_formset.instance = self.object
            version_formset.save()
            return super().form_valid(form)
        # иначе возвращаем ошибку валидации
        else:
            return self.form_invalid(form)

class ProductDeleteView(DeleteView):
    # Указываем модель, для которой создается форма
    model = Product
    # Указываем форму, которая используется для создания объекта
    form_class = ProductForm
    # указываем шаблон
    template_name = 'delete_product.html'
    #у указываем адрес перенаправления
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