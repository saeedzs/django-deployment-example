from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_view

app_name = "useraccounts"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='useraccounts/login.html'), name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('my-order/<int:order_id>/', views.user_order_detail, name='user_order_detail'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='useraccounts/password_reset.html',success_url=reverse_lazy('useraccounts:password_reset_done')), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='useraccounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='useraccounts/password_reset_confirm.html',
                                                                                                success_url=reverse_lazy('useraccounts:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='useraccounts/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change/', auth_view.PasswordChangeView.as_view(template_name='useraccounts/password_change.html',success_url=reverse_lazy('useraccounts:password_change_done')), name='password_change'),
    path('password-change/done/', auth_view.PasswordChangeDoneView.as_view(template_name='useraccounts/password_change_done.html'), name='password_change_done'),
]