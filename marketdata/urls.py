from django.urls import path

from . import views

app_name='marketdata'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('/currency/<int:pk>/', views.CurrencyView.as_view(), name='currency'),
]
