from django.urls import path
from .views import DeactivateAccountView, DeleteAccountView, RegisterView, LoginView, LogoutView, RequestPasswordResetView, UserProfileView, VerifyEmailView, PasswodResetConfirmView, ReactivateAccountView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('request-reset-password/', RequestPasswordResetView.as_view(), name='password-reset-request'),
    path('reset-password/<int:uid>/<str:token>/', PasswodResetConfirmView.as_view(), name='password-reset-confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('deactivate/', DeactivateAccountView.as_view(), name='deactivate-account'),
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
    path('reactivate/', ReactivateAccountView.as_view(), name='reactivate-account'),

]