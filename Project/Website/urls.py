from django.urls import path
from . import views
from .views import PostList

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('', PostList.as_view(), name='home'),
    path('add_post/', views.add_post, name='add_post'),
]