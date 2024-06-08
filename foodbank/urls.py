from django.urls import path
from django.contrib.auth.views import LoginView
from .views import home_view, volunteer_view, volunteer_edit_view, volunteer_delete, foodbank_view, foodbank_delete, \
    task_view, task_delete, individual_shift_view, individual_shift_edit_view, individual_shift_delete

urlpatterns = [
    path('', LoginView.as_view(template_name='home.html'), name='home'),
    #path('', home_view, name='home'),
    path('accounts/login/', LoginView.as_view(template_name='main_page.html', redirect_authenticated_user=False), name='main_page'),
    path('volunteer/', volunteer_view, name='volunteer'),
    path('volunteer/edit/', volunteer_edit_view, name='volunteer_edit'),
    path('volunteer/delete/', volunteer_delete, name='volunteer_delete'),
    path('foodbank/', foodbank_view, name='foodbank'),
    path('foodbank/delete/', foodbank_delete, name='foodbank_delete'),
    path('task/', task_view, name='task'),
    path('task/delete/', task_delete, name='task_delete'),
    path('individual_shift/', individual_shift_view, name='individual_shift'),
    path('individual_shift/edit/', individual_shift_edit_view, name='individual_shift_edit'),
    path('individual_shift/delete/', individual_shift_delete, name='individual_shift_delete'),
    #path('individual_shift/add/', individual_shift_add_view, name='individual_shift_add'),
]
