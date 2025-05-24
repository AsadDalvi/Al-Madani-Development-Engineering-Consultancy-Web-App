from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # User authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    
    # Feedback system
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback_success/', views.feedback_success, name='feedback_success'),
    path('feedback_report/', views.feedback_report, name='feedback_report'),
    path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('download_feedback_report/', views.download_feedback_report, name='download_feedback_report'),

    # Inquiry system
    path('submit_inquiry/', views.submit_inquiry, name='submit_inquiry'),
    path('inquiry_success/', views.inquiry_success, name='inquiry_success'),
    path('inquiry_report/', views.inquiry_report, name='inquiry_report'),
    path('delete_inquiry/<int:inquiry_id>/', views.delete_inquiry, name='delete_inquiry'),
    path('download_inquiry_report/', views.download_inquiry_report, name='download_inquiry_report'),

    # Floor Plan Management (Employee Only)
    path('floor_plans/', views.floor_plans, name='floor_plans'),
    path('floor_plans/upload/', views.upload_floor_plan, name='upload_floor_plan'),
    path('floor_plans/list/', views.floor_plan_list, name='floor_plan_list'),
    path('floor_plans/delete/<int:floor_plan_id>/', views.delete_floor_plan, name='delete_floor_plan'),

    # Home Page
    path('', views.home, name='home'),  
    path('home/', views.home, name='home'), 
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery_view, name='gallery'), 
    path('inquiries/', views.inquiry_report, name='inquiries'),
    path('feedback/', views.submit_feedback, name='feedback'), 
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
