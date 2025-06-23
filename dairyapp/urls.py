from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------
    # Public Routes
    # ----------------------------
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ----------------------------
    # Dashboards (Role-Based)
    # ----------------------------
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('worker_dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),  # ✅ Added this
    path('submit_worker_data/', views.submit_worker_data, name='submit_worker_data'),

    # ----------------------------
    # Admin Features
    # ----------------------------
    path('create_user/', views.create_user_view, name='create_user'),
    path('delete_delivery/<int:delivery_id>/', views.delete_delivery, name='delete_delivery'),
    path('delete_delivery/<int:delivery_id>/', views.delete_delivery, name='delete_delivery'),
    path('delete_milking_log/<int:log_id>/', views.delete_milking_log, name='delete_milking_log'),

]
