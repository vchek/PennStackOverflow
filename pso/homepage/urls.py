from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('faq/', views.faq, name='faq'),
    path('contactus/', views.contactus, name='contact_us'),
]
