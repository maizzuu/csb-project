from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.user, name='user'),
    path('loginView/', views.loginView, name='loginView'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin/', views.admin, name='admin'),
    path('create/', views.create, name='create')
]
