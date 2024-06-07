from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'foodbank'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main_page/', views.main_page_view, name='main_page'),
    path('volunteer/', views.VolunteerView.as_view(), name='volunteer'),
]
