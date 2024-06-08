from django.urls import path
from django.contrib.auth.views import LoginView
from .views import home_view, volunteer_view, volunteer_edit_view, volunteer_delete, foodbank_view, foodbank_delete, \
    task_view, task_delete, individual_shift_view, individual_shift_delete, vehicle_view, vehicle_delete, transit_view, \
    transit_delete, fooditem_view, fooditem_delete, recipient_organization_view, recipient_organization_delete

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
    path('individual_shift/delete/', individual_shift_delete, name='individual_shift_delete'),
    path('vehicle/', vehicle_view, name='vehicle'),
    path('vehicle/delete/', vehicle_delete, name='vehicle_delete'),
    path('transit/', transit_view, name='transit'),
    path('transit/delete/', transit_delete, name='transit_delete'),
    path('fooditem/', fooditem_view, name='fooditem'),
    path('fooditem/delete/', fooditem_delete, name='fooditem_delete'),
    path('recipient_organization/', recipient_organization_view, name='recipient_organization'),
    path('recipient_organization/delete/', recipient_organization_delete, name='recipient_organization_delete'),
]
