from django.urls import path
from django.contrib.auth.views import LoginView
from .views import home_view, volunteer_view, volunteer_edit_view, volunteer_delete, foodbank_view, foodbank_delete

urlpatterns = [
    path('', home_view, name='home'),
    path('accounts/login/', LoginView.as_view(template_name='main_page.html', redirect_authenticated_user=False), name='main_page'),
    path('volunteer/', volunteer_view, name='volunteer'),
    path('volunteer/edit/', volunteer_edit_view, name='volunteer_edit'),
    path('volunteer/delete/', volunteer_delete, name='volunteer_delete'),
    path('foodbank/', foodbank_view, name='foodbank'),
    path('foodbank/delete/', foodbank_delete, name='foodbank_delete'),

]
