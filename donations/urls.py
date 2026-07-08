from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Default page is login
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('request/', views.request_blood, name='request_blood'),
    path('home/', views.home, name='home'),  # move home here

    path('requests/', views.view_requests, name='view_requests'),

    path('requests/fulfill/<int:request_id>/', views.mark_fulfilled, name='mark_fulfilled'),

    

]

