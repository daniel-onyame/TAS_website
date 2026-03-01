from rest_framework import serializers
from django.db import models
from .models import Category, Course, Subject, CourseModule, ExternalResource, CourseReview
from accounts.serializers import TASUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    class Meta:
        model = Category
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model."""
    
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['course']
    
    def create(self, validated_data):
        course = validated_data['course']
        # Auto-assign order if not provided or if it conflicts
        if 'order' not in validated_data or validated_data['order'] == 0:
            # Get the highest order for this course and add 1
            max_order = Subject.objects.filter(course=course).aggregate(
                max_order=models.Max('order')
            )['max_order'] or 0
            validated_data['order'] = max_order + 1
        else:
            # Check if order already exists for this course
            existing_subject = Subject.objects.filter(
                course=course, 
                order=validated_data['order']
            ).first()
            if existing_subject:
                # Shift existing subjects with same or higher order
                Subject.objects.filter(
                    course=course, 
                    order__gte=validated_data['order']
                ).update(order=models.F('order') + 1)
        
        return super().create(validated_data)


class CourseModuleSerializer(serializers.ModelSerializer):
    """Serializer for CourseModule model."""
    
    class Meta:
        model = CourseModule
        fields = '__all__'


class ExternalResourceSerializer(serializers.ModelSerializer):
    """Serializer for ExternalResource model."""
    
    class Meta:
        model = ExternalResource
        fields = '__all__'


class CourseReviewSerializer(serializers.ModelSerializer):
    """Serializer for CourseReview model."""
    
    user = TASUserSerializer(read_only=True)
    
    class Meta:
        model = CourseReview
        fields = '__all__'
        read_only_fields = ['user']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    
    instructor = TASUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    modules = CourseModuleSerializer(many=True, read_only=True)
    external_resources = ExternalResourceSerializer(many=True, read_only=True)
    reviews = CourseReviewSerializer(many=True, read_only=True)
    enrollment_percentage = serializers.ReadOnlyField()
    is_enrollment_open = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for Course list view."""
    
    instructor = TASUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    enrollment_percentage = serializers.ReadOnlyField()
    is_enrollment_open = serializers.ReadOnlyField()
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'category', 'instructor',
            'level', 'duration_weeks', 'credits', 'max_students', 'current_students',
            'thumbnail', 'hero_image', 'status', 'start_date', 'end_date', 'is_featured',
            'is_free', 'price', 'enrollment_percentage', 'is_enrollment_open',
            'review_count', 'average_rating', 'created_at'
        ]
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


class CourseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Course."""
    
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'short_description', 'category', 'level',
            'duration_weeks', 'credits', 'max_students', 'syllabus',
            'prerequisites', 'learning_objectives', 'thumbnail', 'hero_image', 'video_intro',
            'start_date', 'end_date', 'enrollment_deadline', 'is_featured',
            'is_free', 'price'
        ]
    
    def create(self, validated_data):
        from django.utils.text import slugify
        validated_data['instructor'] = self.context['request'].user
        # Generate slug from title
        title = validated_data.get('title', '')
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        # Ensure unique slug
        while Course.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        validated_data['slug'] = slug
        return super().create(validated_data)


class CourseUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Course."""
    
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'short_description', 'category', 'level',
            'duration_weeks', 'credits', 'max_students', 'syllabus',
            'prerequisites', 'learning_objectives', 'thumbnail', 'hero_image', 'video_intro',
            'start_date', 'end_date', 'enrollment_deadline', 'status',
            'is_featured', 'is_free', 'price'
        ] 