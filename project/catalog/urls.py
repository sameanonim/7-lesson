from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, ContactsView, ProductDetailView, ProductCreateView, ProductDeleteView, ProductUpdateView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # Use the CBV as_view() method instead of the FBV
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:id>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('post_list', PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)