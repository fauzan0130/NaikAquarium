from django.contrib import auth
from django.urls import path
from django.views.generic.base import View
from . import views
from .views import home
from django.contrib.auth import authenticate, views as auth_views
from .forms import LoginForm, PasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm




urlpatterns = [
    path('', views.home, name="home"),
    path('product_detail/<int:pk>/',
         views.ProductDetailView.as_view(), name='product_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.display_cart, name='display_cart'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('subtract_cart/', views.subtract_cart, name='subtract_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('profile/', views.UserProfile.as_view(),
         name='user_profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('accounts/login', auth_views.LoginView.as_view(template_name='login.html',
                                                                      authentication_form=LoginForm), name='login'),
    path('accounts/logout/',
         auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('checkout/', views.checkout, name='checkout'),
    path('orderplaced/', views.order_placed, name='orderplaced'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html', form_class=UserPasswordResetForm), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='password_reset_confirm.html', form_class=UserSetPasswordForm), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html',
                                                                   form_class=PasswordChangeForm, success_url='/password_changed/'), name='password_change'),
    path('password_changed/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_changed.html'), name='password_changed'),
]