from django.urls import path
from . import views
urlpatterns = [
    path('',views.home.as_view(),name='home'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('dashbord/',views.AdminDashboard.as_view(),name='admin'),
    
    path('department/create/',views. create_department, name='create_department'),
    path('department/<int:department_id>/update/', views.update_department, name='update_department'),
    path('department/<int:department_id>/delete/', views.delete_department, name='delete_department'),
    path('department/', views.department_list, name='department_list'),

    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
]
