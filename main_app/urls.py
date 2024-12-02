from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('newaccount/', views.register, name='newaccount'),
    path('forgetpassword/', views.user_forgetpassword_view, name='forgetpassword'),
    path('resetpassword/', views.user_resetpassword_view, name='resetpassword'),
    path('producthome/', views.product_home_view, name='producthome'),
    path('mobiles/', views.mobiles_view, name='mobiles'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.logout_view, name='logout'),  # Added logout view
]

