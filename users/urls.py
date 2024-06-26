from django.urls import path
from django.contrib.auth import views as auth_views
from .views import join_index

app_name = "users"
urlpatterns=[
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", join_index, name="signup"),
]