from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q

from .models import (
    TASUser, StaffProfile, GalleryCategory, GalleryImage, GalleryImageLike, GalleryImageView,
    AccommodationType, Accommodation, AccommodationReview, AccommodationInquiry, ContactMessage,
    Student
)
from courses.models import Course


User = get_user_model()


class TASUserSerializer(serializers.ModelSerializer):
    """Serializer for TASUser model."""
    
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TASUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'user_type_display', 'phone_number', 'address',
            'date_of_birth', 'profile_picture', 'bio', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class TASUserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating TASUser model (admin only)."""
    
    class Meta:
        model = TASUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'user_type', 
            'phone_number', 'address', 'date_of_birth', 'profile_picture', 'bio'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=TASUser.USER_TYPE_CHOICES)
    
    class Meta:
        model = TASUser
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type', 'phone_number',
            'address', 'date_of_birth', 'bio', 'profile_picture'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = TASUser.objects.create_user(**validated_data)
        
        # Create profile based on user type
        if user.user_type == 'staff':
            StaffProfile.objects.create(
                user=user,
                staff_id=f"STA{user.id:06d}"
            )
        
        return user


class LoginSerializer11111111(serializers.Serializer):
    """Serializer for user login."""
    
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password.')
        
        return attrs
    
class LoginSerializer22222222(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user_obj = User.objects.get(
                Q(username=username) | Q(email=username)
            )
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials.')

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        attrs['user'] = user
        return attrs
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Username or email"
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"}
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Try username login first
        user = authenticate(username=username, password=password)

        # If not found, try email login
        if not user:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError("Invalid username/email or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        attrs["user"] = user
        return attrs
    

class LoginSerializer444444444(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({
                "detail": "Invalid username or password"
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "detail": "Account is inactive"
            })

        attrs["user"] = user
        return attrs
    


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value




class StaffProfileSerializer(serializers.ModelSerializer):
    """Serializer for StaffProfile model."""
    
    user = TASUserSerializer(read_only=True)
    
    class Meta:
        model = StaffProfile
        fields = '__all__'
        read_only_fields = ['user', 'hire_date', 'staff_id']
    
    def create(self, validated_data):
        # Auto-generate staff_id if not provided
        if 'staff_id' not in validated_data:
            user = validated_data['user']
            validated_data['staff_id'] = f"STA{user.id:06d}"
        return super().create(validated_data)
    
    def validate_position(self, value):
        # Allow empty position for now, but could be made required later
        return value or ''
    
    def validate_department(self, value):
        # Ensure department is always a valid choice
        if not value:
            return 'it'  # Default to IT department
        return value


class TASUserWithStaffSerializer(serializers.ModelSerializer):
    """Serializer for TASUser model with staff profile."""
    
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    staff_profile = StaffProfileSerializer(read_only=True)
    
    class Meta:
        model = TASUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'user_type_display', 'phone_number', 'address',
            'date_of_birth', 'profile_picture', 'bio', 'is_active',
            'created_at', 'updated_at', 'staff_profile'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username




class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile with related profile data."""
    
    staff_profile = StaffProfileSerializer(read_only=True)
    
    class Meta:
        model = TASUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'address', 'date_of_birth',
            'profile_picture', 'bio', 'is_active', 'created_at', 'updated_at',
            'staff_profile'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GalleryCategorySerializer(serializers.ModelSerializer):
    """Serializer for GalleryCategory model."""
    
    image_count = serializers.ReadOnlyField()
    #image_count = serializers.SerializerMethodField()
    icon_display = serializers.CharField(source='get_icon_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = GalleryCategory
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'icon_display', 
            'color', 'is_active', 'display_order', 'image_count',
            'created_at', 'updated_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'created_by']

    def get_image_count(self, obj): # Adjust to your related name return obj.images.count()
        return obj.images.count()


    def create(self, validated_data):
        from django.utils.text import slugify
        validated_data['created_by'] = self.context['request'].user
        # Auto-generate slug from name
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        from django.utils.text import slugify
        # Auto-generate slug from name if name is being updated
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)


class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for GalleryImage model."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    tag_list = serializers.ReadOnlyField()
    image_url = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'description', 'image', 'image_url', 'category', 
            'category_name', 'category_icon', 'category_color', 'location', 
            'date_taken', 'photographer', 'tags', 'tag_list', 'alt_text',
            'is_featured', 'is_active', 'display_order', 'views_count', 
            'likes_count', 'is_liked_by_user', 'created_at', 'updated_at',
            'created_by', 'created_by_name'
        ]
        read_only_fields = [
            'id', 'views_count', 'likes_count', 'created_at', 'updated_at', 'created_by'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                try:
                    return request.build_absolute_uri(obj.image.url)
                except:
                    # Fallback to relative URL if build_absolute_uri fails
                    return obj.image.url
            return obj.image.url
        return None
    
    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_likes.filter(user=request.user).exists()
        return False
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class GalleryImageLikeSerializer(serializers.ModelSerializer):
    """Serializer for GalleryImageLike model."""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    image_title = serializers.CharField(source='image.title', read_only=True)
    
    class Meta:
        model = GalleryImageLike
        fields = ['id', 'image', 'image_title', 'user', 'user_name', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class GalleryImageViewSerializer(serializers.ModelSerializer):
    """Serializer for GalleryImageView model."""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    image_title = serializers.CharField(source='image.title', read_only=True)
    
    class Meta:
        model = GalleryImageView
        fields = [
            'id', 'image', 'image_title', 'user', 'user_name', 
            'ip_address', 'user_agent', 'viewed_at'
        ]
        read_only_fields = ['id', 'user', 'viewed_at']


class GalleryStatsSerializer(serializers.Serializer):
    """Serializer for gallery statistics."""
    
    total_images = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    featured_images = serializers.IntegerField()
    recent_images = serializers.IntegerField()
    popular_categories = serializers.ListField()
    recent_activity = serializers.ListField()


# Icon choices serializer for frontend
class IconChoicesSerializer(serializers.Serializer):
    """Serializer to provide available icon choices."""
    
    value = serializers.CharField()
    label = serializers.CharField()


# Accommodation Serializers
class AccommodationTypeSerializer(serializers.ModelSerializer):
    """Serializer for AccommodationType model."""
    
    accommodation_count = serializers.SerializerMethodField()
    icon_display = serializers.CharField(source='get_icon_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = AccommodationType
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'icon_display', 
            'color', 'is_active', 'display_order', 'accommodation_count',
            'created_at', 'updated_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'created_by']
    
    def get_accommodation_count(self, obj):
        return obj.accommodations.filter(is_active=True).count()
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        from django.utils.text import slugify
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        from django.utils.text import slugify
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)


class AccommodationSerializer(serializers.ModelSerializer):
    """Serializer for Accommodation model."""
    
    accommodation_type_name = serializers.CharField(source='accommodation_type.name', read_only=True)
    accommodation_type_icon = serializers.CharField(source='accommodation_type.icon', read_only=True)
    accommodation_type_color = serializers.CharField(source='accommodation_type.color', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    capacity_text = serializers.CharField(read_only=True)
    price_display = serializers.CharField(read_only=True)
    amenity_list = serializers.ReadOnlyField()
    feature_list = serializers.ReadOnlyField()
    highlight_list = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Accommodation
        fields = [
            'id', 'name', 'slug', 'description', 'accommodation_type', 
            'accommodation_type_name', 'accommodation_type_icon', 'accommodation_type_color',
            'price', 'period', 'price_display', 'location', 'distance_from_campus',
            'capacity_min', 'capacity_max', 'capacity_description', 'capacity_text',
            'main_image', 'main_image_url', 'image_gallery', 'rating', 'reviews_count',
            'availability', 'contact_phone', 'contact_email', 'contact_person',
            'features', 'feature_list', 'amenities', 'amenity_list', 'highlights', 'highlight_list',
            'is_featured', 'is_active', 'display_order', 'created_at', 'updated_at',
            'created_by', 'created_by_name'
        ]
        read_only_fields = ['id', 'slug', 'rating', 'reviews_count', 'created_at', 'updated_at', 'created_by']
    
    def get_main_image_url(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return None
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        from django.utils.text import slugify
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        from django.utils.text import slugify
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)


class AccommodationReviewSerializer(serializers.ModelSerializer):
    """Serializer for AccommodationReview model."""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    accommodation_name = serializers.CharField(source='accommodation.name', read_only=True)
    
    class Meta:
        model = AccommodationReview
        fields = [
            'id', 'accommodation', 'accommodation_name', 'user', 'user_name',
            'rating', 'title', 'comment', 'is_verified', 'is_approved',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AccommodationInquirySerializer(serializers.ModelSerializer):
    """Serializer for AccommodationInquiry model."""
    
    accommodation_name = serializers.CharField(source='accommodation.name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = AccommodationInquiry
        fields = [
            'id', 'accommodation', 'accommodation_name', 'user', 'user_name',
            'name', 'email', 'phone', 'message', 'preferred_contact_method',
            'status', 'is_urgent', 'notes', 'created_at', 'updated_at',
            'contacted_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'contacted_at']
    
    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class AccommodationStatsSerializer(serializers.Serializer):
    """Serializer for accommodation statistics."""
    
    total_accommodations = serializers.IntegerField()
    total_types = serializers.IntegerField()
    total_reviews = serializers.IntegerField()
    total_inquiries = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    featured_accommodations = serializers.IntegerField()
    available_accommodations = serializers.IntegerField()
    popular_types = serializers.ListField()
    recent_accommodations = serializers.ListField()


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model."""
    
    inquiry_type_display = serializers.CharField(source='get_inquiry_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'inquiry_type', 'inquiry_type_display',
            'subject', 'message', 'status', 'status_display', 'is_urgent', 'is_read',
            'admin_notes', 'created_at', 'updated_at', 'read_at', 'replied_at',
            'user', 'user_name'
        ]
        read_only_fields = [
            'id', 'status', 'is_read', 'admin_notes', 'created_at', 'updated_at',
            'read_at', 'replied_at', 'user'
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating ContactMessage (public form)."""
    
    class Meta:
        model = ContactMessage
        fields = [
            'name', 'email', 'phone', 'inquiry_type', 'subject', 'message'
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


# Student Serializers
class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model."""
    
    full_name = serializers.ReadOnlyField()
    student_photo_url = serializers.SerializerMethodField()
    valid_card_photo_url = serializers.SerializerMethodField()
    status_display = serializers.ReadOnlyField()
    sex_display = serializers.ReadOnlyField()
    marital_status_display = serializers.ReadOnlyField()
    education_level_display = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'hometown', 'sex', 'sex_display',
            'occupation', 'marital_status', 'marital_status_display', 'email_address',
            'education_level', 'education_level_display', 'telephone_number',
            'guarantee_name', 'guarantee_number', 'student_photo', 'student_photo_url',
            'valid_card_photo', 'valid_card_photo_url', 'student_id', 'registration_date',
            'status', 'status_display', 'notes', 'is_active', 'created_at', 'updated_at',
            'created_by', 'created_by_name'
        ]
        read_only_fields = [
            'id', 'student_id', 'registration_date', 'created_at', 'updated_at', 'created_by'
        ]
    
    def get_student_photo_url(self, obj):
        if obj.student_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.student_photo.url)
            return obj.student_photo.url
        return None
    
    def get_valid_card_photo_url(self, obj):
        if obj.valid_card_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.valid_card_photo.url)
            return obj.valid_card_photo.url
        return None
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Student (public form)."""
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'hometown', 'sex', 'occupation', 'marital_status',
            'email_address', 'education_level', 'telephone_number', 'guarantee_name',
            'guarantee_number', 'student_photo', 'valid_card_photo', 'notes'
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class StudentStatsSerializer(serializers.Serializer):
    """Serializer for student statistics."""
    
    total_students = serializers.IntegerField()
    pending_students = serializers.IntegerField()
    approved_students = serializers.IntegerField()
    enrolled_students = serializers.IntegerField()
    rejected_students = serializers.IntegerField()
    active_students = serializers.IntegerField()
    recent_registrations = serializers.IntegerField()
    students_by_sex = serializers.DictField()
    students_by_education = serializers.DictField()
    students_by_status = serializers.DictField()
    recent_students = serializers.ListField()