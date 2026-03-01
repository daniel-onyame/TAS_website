from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'gallery/categories', views.GalleryCategoryViewSet, basename='gallery-categories')
router.register(r'gallery/images', views.GalleryImageViewSet, basename='gallery-images')
router.register(r'accommodation/types', views.AccommodationTypeViewSet, basename='accommodation-types')
router.register(r'accommodations', views.AccommodationViewSet, basename='accommodations')
router.register(r'accommodation/reviews', views.AccommodationReviewViewSet, basename='accommodation-reviews')
router.register(r'accommodation/inquiries', views.AccommodationInquiryViewSet, basename='accommodation-inquiries')
router.register(r'contact/messages', views.ContactMessageViewSet, basename='contact-messages')
router.register(r'students', views.StudentViewSet, basename='students')

urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # Role-specific profile endpoints
    path('profile/staff/', views.StaffProfileView.as_view(), name='staff-profile'),
    path('profile/staff/<int:user_id>/', views.AdminStaffProfileView.as_view(), name='admin-staff-profile'),
    
    # Admin user management endpoints
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Staff dashboard endpoints
    path('staff/dashboard/stats/', views.get_staff_dashboard_stats, name='staff-dashboard-stats'),
    
    # Gallery endpoints
    path('gallery/stats/', views.get_gallery_stats, name='gallery-stats'),
    path('gallery/icon-choices/', views.get_gallery_icon_choices, name='gallery-icon-choices'),
    path('gallery/categories/list/', views.get_gallery_categories, name='gallery-categories-list'),
    path('gallery/images/list/', views.get_gallery_images, name='gallery-images-list'),
    
    # Accommodation endpoints
    path('accommodation/stats/', views.get_accommodation_stats, name='accommodation-stats'),
    path('accommodation/icon-choices/', views.get_accommodation_icon_choices, name='accommodation-icon-choices'),
    path('accommodation/amenity-choices/', views.get_accommodation_amenity_choices, name='accommodation-amenity-choices'),
    path('accommodation/types/list/', views.get_accommodation_types, name='accommodation-types-list'),
    path('accommodations/list/', views.get_accommodations, name='accommodations-list'),
    
    # Contact endpoints
    path('contact/submit/', views.submit_contact_message, name='submit-contact-message'),
    
    # Student endpoints
    path('student/stats/', views.get_student_stats, name='student-stats'),
    path('student/choices/', views.get_student_choices, name='student-choices'),
    path('students/list/', views.get_students, name='students-list'),
    path('student/register/', views.submit_student_registration, name='submit-student-registration'),
    
    # Utility endpoints
    path('user-types/', views.get_user_types, name='user-types'),
    path('user-info/', views.get_user_info, name='user-info'),
    path('system-stats/', views.get_system_stats, name='system-stats'),
    
    # Include router URLs
    #path('', include(router.urls)),
    path('', views.index, name='index'),  # Root URL for testing
] 