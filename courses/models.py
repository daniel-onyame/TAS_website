from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Course category model."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    icon = models.CharField(max_length=50, blank=True, null=True)
    hero_image = models.ImageField(upload_to='category_heroes/', blank=True, null=True, help_text='Hero banner image for category detail page')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """Course model for TAS School Management System."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    ]
    
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    
    # Course details
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration_weeks = models.IntegerField(default=12)
    credits = models.IntegerField(default=3)
    max_students = models.IntegerField(default=30)
    current_students = models.IntegerField(default=0)
    
    # Course content
    syllabus = models.TextField(blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    learning_objectives = models.TextField(blank=True, null=True)
    
    # Course media
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='course_heroes/', blank=True, null=True, help_text='Hero banner image for course detail page')
    video_intro = models.URLField(blank=True, null=True)
    
    # Course status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    enrollment_deadline = models.DateField(blank=True, null=True)
    
    # Course settings
    is_featured = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_enrollment_open(self):
        """Check if course enrollment is open."""
        from django.utils import timezone
        today = timezone.now().date()
        return (
            self.status == 'active' and
            (not self.enrollment_deadline or today <= self.enrollment_deadline) and
            self.current_students < self.max_students
        )
    
    @property
    def enrollment_percentage(self):
        """Calculate enrollment percentage."""
        if self.max_students == 0:
            return 0
        return (self.current_students / self.max_students) * 100


class Subject(models.Model):
    """Subject model for organizing course content into specific subjects."""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class CourseModule(models.Model):
    """Course module model for organizing course content."""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class ExternalResource(models.Model):
    """External learning resources linked to courses."""
    
    RESOURCE_TYPE_CHOICES = [
        ('youtube', 'YouTube'),
        ('udemy', 'Udemy'),
        ('coursera', 'Coursera'),
        ('khan_academy', 'Khan Academy'),
        ('other', 'Other'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='external_resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES, default='other')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class CourseReview(models.Model):
    """Course review and rating model."""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['course', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.user.username} - {self.rating} stars" 