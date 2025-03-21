from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_page, name="logout"),
    path('change-password/', views.change_password, name="change_password"),
    path('my-account/', views.my_account, name='my_account'),
    # path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # path('admin-logout/', views.admin_logout, name="admin-logout"),
]
