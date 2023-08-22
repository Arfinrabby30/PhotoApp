from django.urls import path
from . import views


urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.registerPage, name='register'),

]
