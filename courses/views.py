from rest_framework import status, generics, permissions, filters
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Category, Course, Subject, CourseModule, ExternalResource, CourseReview
from .serializers import (
    CategorySerializer, CourseSerializer, CourseListSerializer, CourseCreateSerializer,
    CourseUpdateSerializer, SubjectSerializer, CourseModuleSerializer, ExternalResourceSerializer,
    CourseReviewSerializer
)


class CategoryListView(generics.ListCreateAPIView):
    """List all categories or create a new category."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific category."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseListView(generics.ListAPIView):
    """List all courses with filtering and search."""
    
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'level', 'instructor', 'is_featured', 'is_free', 'status']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'title', 'price', 'start_date']
    ordering = ['-created_at']


class CourseDetailView(generics.RetrieveAPIView):
    """Retrieve a specific course."""
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CourseCreateView(generics.CreateAPIView):
    """Create a new course (instructors only)."""
    
    serializer_class = CourseCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class CourseUpdateView(generics.UpdateAPIView):
    """Update a course (instructor who created it only)."""
    
    queryset = Course.objects.all()
    serializer_class = CourseUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


class CourseDeleteView(generics.DestroyAPIView):
    """Delete a course (instructor who created it only)."""
    
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


class InstructorCourseListView(generics.ListAPIView):
    """List courses for the authenticated instructor."""
    
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


class CourseModuleListView(generics.ListCreateAPIView):
    """List and create modules for a course."""
    
    serializer_class = CourseModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug)
        return CourseModule.objects.filter(course=course)
    
    def perform_create(self, serializer):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug, instructor=self.request.user)
        serializer.save(course=course)


class CourseModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete a course module."""
    
    serializer_class = CourseModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug, instructor=self.request.user)
        return CourseModule.objects.filter(course=course)


class ExternalResourceListView(generics.ListCreateAPIView):
    """List and create external resources for a course."""
    
    serializer_class = ExternalResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug)
        return ExternalResource.objects.filter(course=course)
    
    def perform_create(self, serializer):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug, instructor=self.request.user)
        serializer.save(course=course)


class ExternalResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete an external resource."""
    
    serializer_class = ExternalResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug, instructor=self.request.user)
        return ExternalResource.objects.filter(course=course)


class CourseReviewListView(generics.ListCreateAPIView):
    """List and create reviews for a course."""
    
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug)
        return CourseReview.objects.filter(course=course, is_approved=True)
    
    def perform_create(self, serializer):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug)
        serializer.save(user=self.request.user, course=course)


class CourseReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete a course review."""
    
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CourseReview.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_courses(request):
    """Get featured courses."""
    courses = Course.objects.filter(status='active', is_featured=True)[:6]
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def free_courses(request):
    """Get free courses."""
    courses = Course.objects.filter(status='active', is_free=True)
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def course_statistics(request, course_slug):
    """Get course statistics."""
    course = get_object_or_404(Course, slug=course_slug)
    
    stats = {
        'total_students': course.current_students,
        'max_students': course.max_students,
        'enrollment_percentage': course.enrollment_percentage,
        'is_enrollment_open': course.is_enrollment_open,
        'total_reviews': course.reviews.filter(is_approved=True).count(),
        'average_rating': 0,
    }
    
    reviews = course.reviews.filter(is_approved=True)
    if reviews:
        stats['average_rating'] = sum(review.rating for review in reviews) / reviews.count()
    
    return Response(stats)


class SubjectListView(generics.ListCreateAPIView):
    """List all subjects for a course or create a new subject.

    Public GET access is allowed so the curriculum can be viewed
    without authentication; write actions require authentication.
    """
    
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        course_slug = self.kwargs['course_slug']
        return Subject.objects.filter(course__slug=course_slug)
    
    def perform_create(self, serializer):
        course_slug = self.kwargs['course_slug']
        course = get_object_or_404(Course, slug=course_slug)
        serializer.validated_data['course'] = course
        serializer.save()


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific subject.

    Public read; write actions require authentication.
    """
    
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        course_slug = self.kwargs['course_slug']
        return Subject.objects.filter(course__slug=course_slug)