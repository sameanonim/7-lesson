from django.shortcuts import render

# Create your views here.

def home(request):
    # здесь вы можете добавить логику для получения контекста
    context = {}
    return render(request, 'home.html', context)

def contacts(request):
    # здесь вы можете добавить логику для получения контекста
    context = {}
    return render(request, 'contacts.html', context)