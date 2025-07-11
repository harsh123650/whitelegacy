from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('suscribe/', views.suscribe_view, name='suscribe'),

    path('guide/', views.guide_view, name='guide'),
    path('subscription_select/', views.subscription_select, name='subscription_select'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('delete-contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('delete-subscription/<int:subscription_id>/', views.delete_subscription, name='delete_subscription'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('download-invoice/<int:payment_id>/', views.download_invoice, name='download_invoice'),
    path('pay/', views.payment_page, name='payment_page'),
    path('payment/success/', views.payment_success, name='payment_success'),
    
    
    

    
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('worker_dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),  
    path('submit_worker_data/', views.submit_worker_data, name='submit_worker_data'),

    path('create_user/', views.create_user_view, name='create_user'),
    
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_delivery/<int:delivery_id>/', views.delete_delivery, name='delete_delivery'),
    path('delete_milking/<int:milking_id>/', views.delete_milking, name='delete_milking'),
    path('delete_health/<int:health_id>/', views.delete_health, name='delete_health'),
    path('delete_invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),

    



]
