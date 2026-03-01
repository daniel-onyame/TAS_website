from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    TASUser, StaffProfile, GalleryCategory, GalleryImage, GalleryImageLike, GalleryImageView,
    AccommodationType, Accommodation, AccommodationReview, AccommodationInquiry, Student
)




class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    verbose_name_plural = 'Staff Profile'




@admin.register(TASUser)
class TASUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'user_type', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'first_name', 'last_name'),
        }),
    )
    
    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        
        if obj.user_type == 'staffs':
            return [StaffProfileInline]
        
        return []




@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id', 'hire_date', 'department', 'position')
    list_filter = ('hire_date', 'department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'staff_id', 'position')
    ordering = ('-hire_date',)




@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'color', 'is_active', 'display_order', 'image_count', 'created_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    readonly_fields = ('image_count', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'icon', 'color')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order')
        }),
        ('Metadata', {
            'fields': ('image_count', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_count(self, obj):
        return obj.image_count
    image_count.short_description = 'Images'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'is_featured', 'is_active', 'display_order', 'views_count', 'likes_count', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'date_taken', 'created_at')
    search_fields = ('title', 'description', 'location', 'tags', 'photographer')
    ordering = ('-is_featured', 'display_order', '-created_at')
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at', 'tag_list')
    # list_editable = ('is_featured', 'is_active', 'display_order')  # Temporarily removed
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'category')
        }),
        ('Details', {
            'fields': ('location', 'date_taken', 'photographer', 'tags', 'alt_text')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'display_order')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('tag_list', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def tag_list(self, obj):
        return ', '.join(obj.tag_list) if obj.tag_list else 'No tags'
    tag_list.short_description = 'Tags List'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(GalleryImageLike)
class GalleryImageLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'image__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(GalleryImageView)
class GalleryImageViewAdmin(admin.ModelAdmin):
    list_display = ('image', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('image__title', 'user__username', 'ip_address')
    ordering = ('-viewed_at',)
    readonly_fields = ('viewed_at',)
    
    def has_add_permission(self, request):
        return False  # Views are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Views should not be edited


# ContactMessage is registered in tas_school/admin.py with the custom admin site


# Student model is registered in tas_school/admin.py with the custom admin site



