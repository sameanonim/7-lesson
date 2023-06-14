from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div
from django.forms.widgets import ClearableFileInput
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Version

BANNED_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

def check_banned_words(value):
    # приводим строку к нижнему регистру и разбиваем на слова
    words = value.lower().split()
    # перебираем слова и проверяем, есть ли они в списке запрещенных
    for word in words:
        if word in BANNED_WORDS:
            # если есть, возвращаем сообщение об ошибке
            return f"Слово '{word}' запрещено для использования."

class ProductForm(forms.ModelForm):
    # добавляем валидаторы для полей name и description с кастомными сообщениями об ошибках
    name = forms.CharField(validators=[check_banned_words], error_messages={'invalid': check_banned_words})
    description = forms.CharField(widget=forms.Textarea, validators=[check_banned_words], error_messages={'invalid': check_banned_words})
    image = forms.ImageField(required=False)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    # метод для стилизации формы с помощью crispy-forms
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.prefix = 'product'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('price', css_class='form-group col-md-6 mb-0'),
                Column('image', widget=ClearableFileInput, css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

class ProductDeleteForm(forms.ModelForm):
    # определяем поля и метаданные для формы удаления продукта
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['number_version', 'name_version', 'is_current']

    # метод для стилизации формы с помощью crispy-forms
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.prefix = 'version'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('number_version', css_class='form-group col-md-4 mb-0'),
                Column('name_version', css_class='form-group col-md-4 mb-0'),
                Column('is_current', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )

class VersionForHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = 'bootstrap4/table_inline_formset.html'
        self.form_tag = False
        self.form_show_labels = False

class VersionCreateForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['number_version', 'name_version', 'is_current']

# создаем формсет для версий продукта, связанный с продуктом
VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
