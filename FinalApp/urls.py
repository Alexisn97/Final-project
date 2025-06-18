from django.urls import path
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('all_blogs/', views.blog_list, name='blog_list'),
    path('add_blog/', views.blog_create, name='blog_create'),
    path('edit_blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('delete_blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    path('restricted_page', views.restricted_page, name='Restricted_page'),
    path('restircted_user/<int:user_id>/', views.user_restricted, name='user_restricted'),

]
