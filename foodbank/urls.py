from django.urls import path
from django.contrib.auth.views import LoginView
from .views import home_view, volunteer_view

urlpatterns = [
    path('', home_view, name='home'),
    path('main_page/', LoginView.as_view(template_name='main_page.html', redirect_authenticated_user=False), name='main_page'),
    path('volunteer/', volunteer_view, name='volunteer'),
]
