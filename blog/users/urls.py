from django.urls import path
from .views import UserAccountHandler, updatePassword, login_view, logout_view

urlpatterns = [
    path('signup', UserAccountHandler.as_view()),
    path('<str:username>/', updatePassword, name='update_password'), 
    path('login', login_view, name='login_view'), 
    path('logout', logout_view, name='logout_view')
]