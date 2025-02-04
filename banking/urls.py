from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.func),
    path('create/', views.create, name="create"),
    path('login/', views.login, name="login"),
    path('profile/<str:adhr>/', views.profile, name="profile"),
    path('about/<str:adhr>/',views.about,name="about"),
    path('transfer/<str:adhr>/',views.transfer,name="transfer"),
    path('hist/<str:adhr>/',views.hist,name="hist"),
    path('loan/<str:adhr>/',views.loan,name="loan"),
    path('update/<str:adhr>/',views.update,name="update")
]