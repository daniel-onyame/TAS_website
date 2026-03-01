from django.contrib import admin
from .models import Category, Course, Subject, CourseModule, ExternalResource, CourseReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'icon', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'status', 'level', 'is_featured', 'is_free', 'created_at']
    list_filter = ['status', 'level', 'category', 'is_featured', 'is_free', 'created_at']
    search_fields = ['title', 'description', 'short_description']
    ordering = ['-created_at']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'category', 'instructor')
        }),
        ('Course Details', {
            'fields': ('level', 'duration_weeks', 'credits', 'max_students', 'current_students')
        }),
        ('Content', {
            'fields': ('syllabus', 'prerequisites', 'learning_objectives', 'thumbnail', 'video_intro')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'enrollment_deadline')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'is_free', 'price')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'course', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    ordering = ['course', 'order']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'course', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    ordering = ['course', 'order']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ExternalResource)
class ExternalResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'resource_type', 'is_active', 'created_at']
    list_filter = ['resource_type', 'is_active', 'course', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['course__title', 'user__username', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
