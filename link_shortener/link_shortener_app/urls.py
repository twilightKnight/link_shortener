from django.urls import path
from . import views

app_name = 'link_shortener_app'
urlpatterns = [
    path('features/', views.features, name='features'),
    path('sign_up/', views.create_new_user_account, name='sign_up'),
    path('sign_in/', views.sign_in_account, name='sign_in'),
    path('<str:short_link>/', views.redirect_, name='redirect'),
    path('', views.index, name='index'),
]
