from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Courses
    path('', views.CourseListView.as_view(), name='course-list'),
    path('featured/', views.featured_courses, name='featured-courses'),
    path('free/', views.free_courses, name='free-courses'),
    path('create/', views.CourseCreateView.as_view(), name='course-create'),
    path('my-courses/', views.InstructorCourseListView.as_view(), name='instructor-courses'),
    path('subjects/', views.CategoryListView.as_view(), name='all-subject-list'),

    # Course Details and Management
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('<slug:slug>/update/', views.CourseUpdateView.as_view(), name='course-update'),
    path('<slug:slug>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    path('<slug:slug>/statistics/', views.course_statistics, name='course-statistics'),
    
    # Course Subjects
    path('<slug:course_slug>/subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('<slug:course_slug>/subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    
    # Course Modules
    path('<slug:course_slug>/modules/', views.CourseModuleListView.as_view(), name='module-list'),
    path('<slug:course_slug>/modules/<int:pk>/', views.CourseModuleDetailView.as_view(), name='module-detail'),
    
    # External Resources
    path('<slug:course_slug>/resources/', views.ExternalResourceListView.as_view(), name='resource-list'),
    path('<slug:course_slug>/resources/<int:pk>/', views.ExternalResourceDetailView.as_view(), name='resource-detail'),
    
    # Course Reviews
    path('<slug:course_slug>/reviews/', views.CourseReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.CourseReviewDetailView.as_view(), name='review-detail'),
] 