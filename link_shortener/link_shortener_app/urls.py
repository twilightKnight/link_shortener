from django.urls import path
from . import views

app_name = 'link_shortener_app'
urlpatterns = [
    path('change_state/<slug:short_link>/<str:clicks_mode>', views.LinkUpdate.as_view(), name='link_update'),
    path('verification/', views.EmailVerifier.as_view(), name='email_verifier'),
    path('features/', views.features, name='features'),
    path('user_page/', views.UserPage.as_view(), name='user_page'),
    path('register/', views.CreateUser.as_view(), name='register'),
    path('sign_in/', views.SignInAccount.as_view(), name='sign_in'),
    path('<slug:short_link>/', views.Redirect.as_view(), name='redirect'),
    path('', views.Index.as_view(), name='index'),
]

