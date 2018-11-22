from django.urls import path
#to show which thing to view need to import views
from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('demo/', views.demo_from, name='demo_form'),
    path('signup/', views.sign_up, name='sign_up'),
    path('currentusers/', views.current_users, name='current_users'),
    path('registration/', views.registration_form, name='registration_form'),
    path('login/', views.login_form, name = 'login_form'),
    path('logout/', views.logout_page, name='logout_page'),
]
