from django.urls import include, path, re_path

from . import views

user_urlpatterns = [
    path('signup/', views.signup_user, name='user_signup'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset-done/', views.password_reset_done,
         name='account_reset_password_done'),
    re_path(
        r'^reset-password-from-key/(?P<uidb36>[\dA-Za-z]+)-(?P<key>.+)/$',
        views.password_reset_from_key,
        name='account_reset_password_from_key'
    ),
    path('reset-password-from-key-done/', views.password_reset_from_key_done,
         name='account_reset_password_from_key_done'),
    path('password-change/', views.change_password, name='password_change')
]

urlpatterns = [
    path('user/', include(user_urlpatterns)),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('administrator/signup/', views.signup_administrator,
         name='administrator_signup'),
    path('confirm-email-sent/', views.email_verification_sent,
         name='account_email_verification_sent'),
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$', views.confirm_email,
            name='account_confirm_email'),
    path('profile/', views.check, name='profile'),
]
