from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import (
    TASUser, StaffProfile, GalleryCategory, GalleryImage, GalleryImageLike, GalleryImageView,
    AccommodationType, Accommodation, AccommodationReview, AccommodationInquiry, ContactMessage,
    Student
)
from courses.models import Category, Course, Subject, CourseModule, ExternalResource, CourseReview

# Get the custom user model
User = get_user_model()

# Create a custom admin site
class TASAdminSite(admin.AdminSite):
    site_header = "TAS School Management System"
    site_title = "TAS School Admin"
    index_title = "Welcome to TAS School Management System"
    
    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        the admin site.
        """
        return request.user.is_active and request.user.is_staff
    

# Create the admin site instance
admin_site = TASAdminSite(name='tas_admin')

# Register the user model with the custom admin site
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_superuser', 'created_at')
    list_filter = ('user_type', 'is_active', 'is_superuser', 'created_at', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'bio')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'Django superusers have full system access. TAS users have limited permissions.'
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id', 'department', 'position', 'hire_date')
    list_filter = ('department', 'hire_date')
    search_fields = ('user__username', 'staff_id', 'position')
    readonly_fields = ('staff_id', 'hire_date')


class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color', 'is_active', 'display_order', 'created_by', 'created_at')
    list_filter = ('is_active', 'created_at', 'created_by')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'display_order')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'is_featured', 'is_active', 'display_order', 'views_count', 'likes_count', 'created_by', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at', 'created_by')
    search_fields = ('title', 'description', 'location', 'tags')
    list_editable = ('is_featured', 'is_active', 'display_order')
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class GalleryImageLikeAdmin(admin.ModelAdmin):
    list_display = ('image', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('image__title', 'user__username')
    readonly_fields = ('created_at',)


class GalleryImageViewAdmin(admin.ModelAdmin):
    list_display = ('image', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('image__title', 'user__username', 'ip_address')
    readonly_fields = ('viewed_at',)
    
    def has_add_permission(self, request):
        return False  # Views are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Views should not be edited


# Accommodation Admin Classes
class AccommodationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color', 'is_active', 'display_order', 'created_by', 'created_at')
    list_filter = ('is_active', 'created_at', 'created_by')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'display_order')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'accommodation_type', 'price', 'period', 'location', 'availability', 'is_featured', 'is_active', 'display_order', 'rating', 'created_by', 'created_at')
    list_filter = ('accommodation_type', 'availability', 'is_featured', 'is_active', 'created_at', 'created_by')
    search_fields = ('name', 'description', 'location')
    list_editable = ('is_featured', 'is_active', 'display_order', 'availability')
    readonly_fields = ('slug', 'rating', 'reviews_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'accommodation_type', 'main_image')
        }),
        ('Pricing', {
            'fields': ('price', 'period')
        }),
        ('Location', {
            'fields': ('location', 'distance_from_campus')
        }),
        ('Capacity', {
            'fields': ('capacity_min', 'capacity_max', 'capacity_description')
        }),
        ('Status & Features', {
            'fields': ('availability', 'is_featured', 'is_active', 'display_order')
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'contact_person')
        }),
        ('Features & Amenities', {
            'fields': ('features', 'amenities', 'highlights'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('rating', 'reviews_count', 'created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class AccommodationReviewAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'user', 'rating', 'title', 'is_verified', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_verified', 'is_approved', 'created_at')
    search_fields = ('accommodation__name', 'user__username', 'title', 'comment')
    list_editable = ('is_verified', 'is_approved')
    readonly_fields = ('created_at', 'updated_at')


class AccommodationInquiryAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'name', 'email', 'phone', 'status', 'is_urgent', 'created_at')
    list_filter = ('status', 'is_urgent', 'created_at')
    search_fields = ('accommodation__name', 'name', 'email', 'phone')
    list_editable = ('status', 'is_urgent')
    readonly_fields = ('created_at', 'updated_at', 'contacted_at')
    
    fieldsets = (
        ('Inquiry Details', {
            'fields': ('accommodation', 'name', 'email', 'phone', 'message', 'preferred_contact_method')
        }),
        ('Status & Management', {
            'fields': ('status', 'is_urgent', 'notes', 'contacted_at')
        }),
        ('Metadata', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry_type', 'subject', 'status', 'is_urgent', 'created_at')
    list_filter = ('inquiry_type', 'status', 'is_urgent', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'read_at', 'replied_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'user')
        }),
        ('Message Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Status & Management', {
            'fields': ('status', 'is_urgent', 'is_read', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'read_at', 'replied_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_closed']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True, status='read')
        self.message_user(request, f'{updated} messages marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} messages marked as replied.')
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} messages marked as closed.')
    mark_as_closed.short_description = "Mark selected messages as closed"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'student_id', 'email_address', 'sex', 'education_level', 'status', 'is_active', 'registration_date')
    list_filter = ('status', 'sex', 'education_level', 'marital_status', 'occupation', 'is_active', 'registration_date', 'created_at')
    search_fields = ('first_name', 'last_name', 'email_address', 'student_id', 'hometown', 'guarantee_name', 'telephone_number')
    ordering = ('-created_at',)
    readonly_fields = ('student_id', 'registration_date', 'created_at', 'updated_at', 'get_full_name', 'student_photo_url', 'valid_card_photo_url')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'get_full_name', 'hometown', 'sex', 'marital_status', 'occupation')
        }),
        ('Contact Information', {
            'fields': ('email_address', 'telephone_number')
        }),
        ('Education & Background', {
            'fields': ('education_level',)
        }),
        ('Guarantor Information', {
            'fields': ('guarantee_name', 'guarantee_number')
        }),
        ('Photo Uploads', {
            'fields': ('student_photo', 'student_photo_url', 'valid_card_photo', 'valid_card_photo_url'),
            'classes': ('collapse',)
        }),
        ('Registration Details', {
            'fields': ('student_id', 'registration_date', 'status', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Full Name'
    
    def student_photo_url(self, obj):
        if obj.student_photo:
            return obj.student_photo.url
        return 'No photo uploaded'
    student_photo_url.short_description = 'Student Photo URL'
    
    def valid_card_photo_url(self, obj):
        if obj.valid_card_photo:
            return obj.valid_card_photo.url
        return 'No photo uploaded'
    valid_card_photo_url.short_description = 'ID Card Photo URL'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['approve_students', 'reject_students', 'enroll_students', 'mark_as_active', 'mark_as_inactive']
    
    def approve_students(self, request, queryset):
        """Approve selected students."""
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} students were successfully approved.')
    approve_students.short_description = "Approve selected students"
    
    def reject_students(self, request, queryset):
        """Reject selected students."""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} students were successfully rejected.')
    reject_students.short_description = "Reject selected students"
    
    def enroll_students(self, request, queryset):
        """Enroll approved students."""
        approved_students = queryset.filter(status='approved')
        updated = approved_students.update(status='enrolled')
        self.message_user(request, f'{updated} students were successfully enrolled.')
    enroll_students.short_description = "Enroll approved students"
    
    def mark_as_active(self, request, queryset):
        """Mark selected students as active."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} students were marked as active.')
    mark_as_active.short_description = "Mark selected students as active"
    
    def mark_as_inactive(self, request, queryset):
        """Mark selected students as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} students were marked as inactive.')
    mark_as_inactive.short_description = "Mark selected students as inactive"


# Register models with the custom admin site
admin_site.register(User, CustomUserAdmin)
admin_site.register(StaffProfile, StaffProfileAdmin)
admin_site.register(GalleryCategory, GalleryCategoryAdmin)
admin_site.register(GalleryImage, GalleryImageAdmin)
admin_site.register(GalleryImageLike, GalleryImageLikeAdmin)
admin_site.register(GalleryImageView, GalleryImageViewAdmin)
admin_site.register(AccommodationType, AccommodationTypeAdmin)
admin_site.register(Accommodation, AccommodationAdmin)
admin_site.register(AccommodationReview, AccommodationReviewAdmin)
admin_site.register(AccommodationInquiry, AccommodationInquiryAdmin)
admin_site.register(ContactMessage, ContactMessageAdmin)
admin_site.register(Student, StudentAdmin)

# Register courses models
admin_site.register(Category)
admin_site.register(Course)
admin_site.register(Subject)
admin_site.register(CourseModule) #ContactMessage
admin_site.register(ExternalResource)
admin_site.register(CourseReview)

#check the backend, I again can see the Contact message in jazzmin. please check the  django admin files and see if they are properly registered.