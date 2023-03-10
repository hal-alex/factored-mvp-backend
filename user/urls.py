"""
URL mappings for the user API
"""

from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path('create/', views.CreateUserView.as_view()),
    path('token/', views.CreateTokenView.as_view()),
    path('me/', views.ManageUserView.as_view()),
    path('forgotpassword/', views.ForgotPasswordView.as_view()),
    path('resetpassword/', views.ResetPasswordView.as_view()),
    path('persona_webhook/', views.webhook),
]
