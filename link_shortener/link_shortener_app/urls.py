from django.urls import path
from . import views

app_name = 'link_shortener_app'
urlpatterns = [
    path('verification/', views.verification_page, name='verification_page'),
    path('features/', views.features, name='features'),
    path('user_page/', views.user_page, name='user_page'),
    path('register/', views.create_new_user_account, name='register'),
    path('sign_in/', views.sign_in_account, name='sign_in'),
    path('<str:short_link>/', views.redirect_, name='redirect'),
    path('', views.index, name='index'),
]

