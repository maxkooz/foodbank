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
    path('volunteers/', views.VolunteerView.as_view(), name='volunteers'),
    path('foodbanks/', views.FoodBankView.as_view(), name='foodbanks'),
    path('tasks/', views.TaskView.as_view(), name='tasks'),
    path('individual_shifts/', views.individual_shift_view, name='individual_shifts'),
    path('individual_shifts/delete/', views.individual_shift_delete, name='individual_shift_delete'),
    path('vehicles/', views.vehicle_view, name='vehicles'),
    path('vehicles/delete/', views.vehicle_delete, name='vehicle_delete'),
    path('transits/', views.transit_view, name='transits'),
    path('transits/delete/', views.transit_delete, name='transit_delete'),
    path('transits/capacity/', views.transit_capacity, name='transit_capacity'),
    path('fooditems/', views.fooditem_view, name='fooditems'),
    path('fooditems/delete/', views.fooditem_delete, name='fooditem_delete'),
    path('recipient_organizations/', views.recipient_organization_view, name='recipient_organizations'),
    path('recipient_organizations/delete/', views.recipient_organization_delete, name='recipient_organization_delete'),
    path('distributed-food-items/', views.distributed_food_item_view, name='distributed_food_items'),
    path('distributed-food-items/delete/', views.distributed_food_item_delete, name='distributed_food_item_delete'),
    path('donators/', views.donator_view, name='donators'),
    path('donators/delete/', views.donator_delete, name='donator_delete'),
    path('foodgroups/', views.foodgroup_view, name='foodgroups'),
    path('foodgroups/delete/', views.foodgroup_delete, name='foodgroup_delete'),
]
