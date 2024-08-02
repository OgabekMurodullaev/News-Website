from django.urls import path
from .views import userlogin, userprofile_view, user_registration, edit_user, AdminPageView, admin_page
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

urlpatterns = [
    #path('login/', userlogin, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-profile/', userprofile_view, name='user_profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('signup/', user_registration, name="signup"),
    path('profile/edit/', edit_user, name="edit_user_information"),
    path('admin-page/', admin_page, name="admin_page"),
    # path('signup/', UserRegisterView.as_view(), name='signup')
]