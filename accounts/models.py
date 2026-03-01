from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError

STAFF_DEPARTMENT_CHOICES = [
        ('it', 'IT'),
        ('business', 'Business'),
        ('language', 'Language'),
        ('administration', 'Administration'),
    ]

class TASUser(AbstractUser):
    """Custom User model for TAS School Management System users."""
    
    USER_TYPE_CHOICES = [
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='staff')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('TAS User')
        verbose_name_plural = _('TAS Users')
        db_table = 'tas_users'
    
    def __str__(self):
        if self.is_superuser:
            return f"{self.username} - Django Superuser"
        return f"{self.username} - {self.get_user_type_display()}"
    
    @property
    def is_django_admin(self):
        """Check if user is a Django admin (full permissions)."""
        return self.is_superuser  # Django superusers have full permissions


class StaffProfile(models.Model):
    """Staff specific profile information."""
    
    user = models.OneToOneField(TASUser, on_delete=models.CASCADE, related_name='staff_profile')
    staff_id = models.CharField(max_length=20, unique=True)
    hire_date = models.DateField(auto_now_add=True)
    department = models.CharField(max_length=100, choices=STAFF_DEPARTMENT_CHOICES, default='it')
    position = models.CharField(max_length=100, blank=True, null=True)
    office_location = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'staff_profiles'
    
    def __str__(self):
        #return f"{self.user.username} - {self.staff_id}"
        return f"{self.user.username}"


# Gallery Icon Choices - Essential icons for categories
GALLERY_ICON_CHOICES = [
    ('FaBuilding', 'Building'),
    ('FaCalendarAlt', 'Calendar'),
    ('FaUsers', 'Users'),
    ('FaGraduationCap', 'Graduation Cap'),
    ('FaBook', 'Book'),
    ('FaImages', 'Images'),
    ('FaHeart', 'Heart'),
    ('FaStar', 'Star'),
    ('FaTrophy', 'Trophy'),
    ('FaMicrophone', 'Microphone'),
    ('FaCamera', 'Camera'),
    ('FaVideo', 'Video'),
    ('FaMusic', 'Music'),
    ('FaGamepad', 'Gamepad'),
    ('FaFootball', 'Football'),
    ('FaSwimmingPool', 'Swimming Pool'),
    ('FaCar', 'Car'),
    ('FaPlane', 'Plane'),
    ('FaGlobe', 'Globe'),
    ('FaMapMarkerAlt', 'Map Marker'),
    ('FaHome', 'Home'),
    ('FaSchool', 'School'),
    ('FaUniversity', 'University'),
    ('FaLaptop', 'Laptop'),
    ('FaDesktop', 'Desktop'),
    ('FaTablet', 'Tablet'),
    ('FaMobile', 'Mobile'),
    ('FaWifi', 'WiFi'),
    ('FaCog', 'Settings'),
    ('FaTools', 'Tools'),
    ('FaLightbulb', 'Lightbulb'),
    ('FaRocket', 'Rocket'),
    ('FaGem', 'Gem'),
    ('FaCrown', 'Crown'),
    ('FaMedal', 'Medal'),
    ('FaAward', 'Award'),
    ('FaCertificate', 'Certificate'),
    ('FaScroll', 'Scroll'),
    ('FaBookOpen', 'Book Open'),
    ('FaPen', 'Pen'),
    ('FaPencil', 'Pencil'),
    ('FaEraser', 'Eraser'),
    ('FaCalculator', 'Calculator'),
    ('FaRuler', 'Ruler'),
    ('FaCompass', 'Compass'),
    ('FaMicroscope', 'Microscope'),
    ('FaFlask', 'Flask'),
    ('FaAtom', 'Atom'),
    ('FaDna', 'DNA'),
    ('FaLeaf', 'Leaf'),
    ('FaTree', 'Tree'),
    ('FaSun', 'Sun'),
    ('FaMoon', 'Moon'),
    ('FaCloud', 'Cloud'),
    ('FaRainbow', 'Rainbow'),
    ('FaSnowflake', 'Snowflake'),
    ('FaFire', 'Fire'),
    ('FaWater', 'Water'),
    ('FaWind', 'Wind'),
    ('FaMountain', 'Mountain'),
    ('FaSea', 'Sea'),
    ('FaFish', 'Fish'),
    ('FaBird', 'Bird'),
    ('FaCat', 'Cat'),
    ('FaDog', 'Dog'),
    ('FaHorse', 'Horse'),
    ('FaPaw', 'Paw'),
    ('FaBug', 'Bug'),
    ('FaSpider', 'Spider'),
    ('FaButterfly', 'Butterfly'),
    ('FaFlower', 'Flower'),
    ('FaSeedling', 'Seedling'),
    ('FaApple', 'Apple'),
    ('FaBanana', 'Banana'),
    ('FaCarrot', 'Carrot'),
    ('FaPizza', 'Pizza'),
    ('FaHamburger', 'Hamburger'),
    ('FaCoffee', 'Coffee'),
    ('FaTea', 'Tea'),
    ('FaBeer', 'Beer'),
    ('FaWine', 'Wine'),
    ('FaCake', 'Cake'),
    ('FaCookie', 'Cookie'),
    ('FaIceCream', 'Ice Cream'),
    ('FaCandy', 'Candy'),
    ('FaGift', 'Gift'),
    ('FaBirthdayCake', 'Birthday Cake'),
    ('FaPartyHorn', 'Party Horn'),
    ('FaBalloon', 'Balloon'),
    ('FaConfetti', 'Confetti'),
    ('FaFireworks', 'Fireworks'),
    ('FaMagic', 'Magic'),
    ('FaWand', 'Wand'),
    ('FaHat', 'Hat'),
    ('FaMask', 'Mask'),
    ('FaGlasses', 'Glasses'),
    ('FaEye', 'Eye'),
    ('FaEar', 'Ear'),
    ('FaNose', 'Nose'),
    ('FaMouth', 'Mouth'),
    ('FaHand', 'Hand'),
    ('FaFist', 'Fist'),
    ('FaThumbsUp', 'Thumbs Up'),
    ('FaThumbsDown', 'Thumbs Down'),
    ('FaPeace', 'Peace'),
    ('FaOk', 'OK'),
    ('FaPointUp', 'Point Up'),
    ('FaPointDown', 'Point Down'),
    ('FaPointLeft', 'Point Left'),
    ('FaPointRight', 'Point Right'),
    ('FaStop', 'Stop'),
    ('FaPlay', 'Play'),
    ('FaPause', 'Pause'),
    ('FaForward', 'Forward'),
    ('FaBackward', 'Backward'),
    ('FaStepForward', 'Step Forward'),
    ('FaStepBackward', 'Step Backward'),
    ('FaFastForward', 'Fast Forward'),
    ('FaFastBackward', 'Fast Backward'),
    ('FaShuffle', 'Shuffle'),
    ('FaRepeat', 'Repeat'),
    ('FaVolumeUp', 'Volume Up'),
    ('FaVolumeDown', 'Volume Down'),
    ('FaVolumeMute', 'Volume Mute'),
    ('FaVolumeOff', 'Volume Off'),
    ('FaHeadphones', 'Headphones'),
    ('FaMicrophoneAlt', 'Microphone Alt'),
    ('FaRadio', 'Radio'),
    ('FaTv', 'TV'),
    ('FaPhone', 'Phone'),
    ('FaFax', 'Fax'),
    ('FaEnvelope', 'Envelope'),
    ('FaMailBulk', 'Mail Bulk'),
    ('FaInbox', 'Inbox'),
    ('FaOutbox', 'Outbox'),
    ('FaArchive', 'Archive'),
    ('FaTrash', 'Trash'),
    ('FaRecycle', 'Recycle'),
    ('FaSave', 'Save'),
    ('FaDownload', 'Download'),
    ('FaUpload', 'Upload'),
    ('FaShare', 'Share'),
    ('FaLink', 'Link'),
    ('FaUnlink', 'Unlink'),
    ('FaCopy', 'Copy'),
    ('FaCut', 'Cut'),
    ('FaPaste', 'Paste'),
    ('FaUndo', 'Undo'),
    ('FaRedo', 'Redo'),
    ('FaSearch', 'Search'),
    ('FaFilter', 'Filter'),
    ('FaSort', 'Sort'),
    ('FaSortUp', 'Sort Up'),
    ('FaSortDown', 'Sort Down'),
    ('FaList', 'List'),
    ('FaTh', 'Grid'),
    ('FaThList', 'Grid List'),
    ('FaBars', 'Bars'),
    ('FaEllipsisH', 'Ellipsis Horizontal'),
    ('FaEllipsisV', 'Ellipsis Vertical'),
    ('FaPlus', 'Plus'),
    ('FaMinus', 'Minus'),
    ('FaTimes', 'Times'),
    ('FaCheck', 'Check'),
    ('FaExclamation', 'Exclamation'),
    ('FaQuestion', 'Question'),
    ('FaInfo', 'Info'),
    ('FaExclamationTriangle', 'Exclamation Triangle'),
    ('FaQuestionCircle', 'Question Circle'),
    ('FaInfoCircle', 'Info Circle'),
    ('FaCheckCircle', 'Check Circle'),
    ('FaTimesCircle', 'Times Circle'),
    ('FaBan', 'Ban'),
    ('FaLock', 'Lock'),
    ('FaUnlock', 'Unlock'),
    ('FaKey', 'Key'),
    ('FaShield', 'Shield'),
    ('FaShieldAlt', 'Shield Alt'),
    ('FaUser', 'User'),
    ('FaUserAlt', 'User Alt'),
    ('FaUserCheck', 'User Check'),
    ('FaUserTimes', 'User Times'),
    ('FaUserPlus', 'User Plus'),
    ('FaUserMinus', 'User Minus'),
    ('FaUserEdit', 'User Edit'),
    ('FaUserCog', 'User Cog'),
    ('FaUserShield', 'User Shield'),
    ('FaUserSecret', 'User Secret'),
    ('FaUserGraduate', 'User Graduate'),
    ('FaUserTie', 'User Tie'),
    ('FaUserNurse', 'User Nurse'),
    ('FaUserMd', 'User MD'),
    ('FaUserInjured', 'User Injured'),
    ('FaUserFriends', 'User Friends'),
    ('FaUserClock', 'User Clock'),
    ('FaUserTag', 'User Tag'),
    ('FaUserSlash', 'User Slash'),
    ('FaUsers', 'Users'),
    ('FaUsersCog', 'Users Cog'),
    ('FaUserCircle', 'User Circle'),
    ('FaIdCard', 'ID Card'),
    ('FaIdCardAlt', 'ID Card Alt'),
    ('FaAddressCard', 'Address Card'),
    ('FaAddressBook', 'Address Book'),
    ('FaPhoneAlt', 'Phone Alt'),
    ('FaPhoneSquare', 'Phone Square'),
    ('FaPhoneSquareAlt', 'Phone Square Alt'),
    ('FaPhoneVolume', 'Phone Volume'),
    ('FaPhoneSlash', 'Phone Slash'),
    ('FaEnvelopeOpen', 'Envelope Open'),
    ('FaEnvelopeSquare', 'Envelope Square'),
]


class GalleryCategory(models.Model):
    """Gallery categories for organizing images."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, choices=GALLERY_ICON_CHOICES, default='FaImages')
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(TASUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_gallery_categories')
    
    class Meta:
        db_table = 'gallery_categories'
        verbose_name = 'Gallery Category'
        verbose_name_plural = 'Gallery Categories'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    #@property
    def image_count(self):
        return self.images.filter(is_active=True).count()


class GalleryImage(models.Model):
    """Gallery images with metadata."""
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/', help_text="Upload gallery image")
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Location where photo was taken")
    date_taken = models.DateField(blank=True, null=True, help_text="Date when photo was taken")
    photographer = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")
    alt_text = models.CharField(max_length=200, blank=True, null=True, help_text="Alternative text for accessibility")
    is_featured = models.BooleanField(default=False, help_text="Featured images appear prominently")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(TASUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_gallery_images')
    
    class Meta:
        db_table = 'gallery_images'
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['-is_featured', 'display_order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        """Increment view count."""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_likes(self):
        """Increment like count."""
        self.likes_count += 1
        self.save(update_fields=['likes_count'])
    
    @property
    def tag_list(self):
        """Return tags as a list."""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class GalleryImageLike(models.Model):
    """Track user likes for gallery images."""
    
    image = models.ForeignKey(GalleryImage, on_delete=models.CASCADE, related_name='user_likes')
    user = models.ForeignKey(TASUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'gallery_image_likes'
        unique_together = ['image', 'user']
        verbose_name = 'Gallery Image Like'
        verbose_name_plural = 'Gallery Image Likes'
    
    def __str__(self):
        return f"{self.user.username} likes {self.image.title}"


class GalleryImageView(models.Model):
    """Track image views for analytics."""
    
    image = models.ForeignKey(GalleryImage, on_delete=models.CASCADE, related_name='view_logs')
    user = models.ForeignKey(TASUser, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'gallery_image_views'
        verbose_name = 'Gallery Image View'
        verbose_name_plural = 'Gallery Image Views'
        ordering = ['-viewed_at']
    
    def __str__(self):
        user_info = self.user.username if self.user else f"Anonymous ({self.ip_address})"
        return f"{user_info} viewed {self.image.title}"


# Accommodation Icon Choices - Essential icons for accommodation types
ACCOMMODATION_ICON_CHOICES = [
    ('FaBuilding', 'Building'),
    ('FaHome', 'Home'),
    ('FaBed', 'Bed'),
    ('FaKey', 'Key'),
    ('FaHotel', 'Hotel'),
    ('FaUniversity', 'University'),
    ('FaSchool', 'School'),
    ('FaUsers', 'Users'),
    ('FaUser', 'Single User'),
    ('FaUserFriends', 'Multiple Users'),
    ('FaMapMarkerAlt', 'Location'),
    ('FaCar', 'Car'),
    ('FaWifi', 'WiFi'),
    ('FaUtensils', 'Kitchen'),
    ('FaShower', 'Bathroom'),
    ('FaParking', 'Parking'),
    ('FaSwimmingPool', 'Swimming Pool'),
    ('FaGamepad', 'Gym'),
    ('FaTree', 'Garden'),
    ('FaSun', 'Air Conditioning'),
    ('FaShieldAlt', 'Security'),
    ('FaHeart', 'Heart'),
    ('FaStar', 'Star'),
    ('FaCheck', 'Check'),
    ('FaTimes', 'Times'),
]

# Accommodation Amenity Choices
ACCOMMODATION_AMENITY_CHOICES = [
    ('wifi', 'WiFi'),
    ('kitchen', 'Kitchen'),
    ('laundry', 'Laundry'),
    ('security', 'Security'),
    ('study', 'Study Room'),
    ('lounge', 'Common Lounge'),
    ('ac', 'Air Conditioning'),
    ('gym', 'Gym'),
    ('parking', 'Parking'),
    ('cafeteria', 'Cafeteria'),
    ('private-bathroom', 'Private Bathroom'),
    ('furnished', 'Furnished'),
    ('balcony', 'Balcony'),
    ('utilities', 'Utilities Included'),
    ('garden', 'Garden'),
    ('shared-living', 'Shared Living'),
    ('social', 'Social Areas'),
    ('budget', 'Budget Friendly'),
    ('cultural', 'Cultural Programs'),
    ('language', 'Language Support'),
    ('travel', 'Travel Assistance'),
    ('orientation', 'Orientation Programs'),
]

class AccommodationType(models.Model):
    """Accommodation type categories (Dormitory, Apartment, Hostel, etc.)"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, choices=ACCOMMODATION_ICON_CHOICES, default='FaBuilding')
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(TASUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'accommodation_types'
        verbose_name = 'Accommodation Type'
        verbose_name_plural = 'Accommodation Types'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_icon_display(self):
        """Get the display name for the icon."""
        for choice in ACCOMMODATION_ICON_CHOICES:
            if choice[0] == self.icon:
                return choice[1]
        return self.icon
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Accommodation(models.Model):
    """Accommodation listings for students."""
    
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('limited', 'Limited'),
        ('full', 'Full'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    accommodation_type = models.ForeignKey(AccommodationType, on_delete=models.CASCADE, related_name='accommodations')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=20, default='month', help_text='per month, per semester, etc.')
    
    # Location
    location = models.CharField(max_length=200)
    distance_from_campus = models.CharField(max_length=100, blank=True, null=True)
    
    # Capacity and Features
    capacity_min = models.PositiveIntegerField(default=1)
    capacity_max = models.PositiveIntegerField(default=1)
    capacity_description = models.CharField(max_length=100, blank=True, null=True)
    
    # Images
    main_image = models.ImageField(upload_to='accommodation_images/', blank=True, null=True)
    image_gallery = models.JSONField(default=list, blank=True, help_text='List of additional image URLs')
    
    # Ratings and Reviews
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    
    # Availability
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    
    # Contact Information
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    
    # Features and Amenities
    features = models.JSONField(default=list, blank=True, help_text='List of feature descriptions')
    amenities = models.JSONField(default=list, blank=True, help_text='List of amenity codes')
    
    # Highlights/Tags
    highlights = models.JSONField(default=list, blank=True, help_text='List of highlight tags')
    
    # Status and Metadata
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(TASUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'accommodations'
        verbose_name = 'Accommodation'
        verbose_name_plural = 'Accommodations'
        ordering = ['-is_featured', 'display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def capacity_text(self):
        """Return formatted capacity text."""
        if self.capacity_description:
            return self.capacity_description
        if self.capacity_min == self.capacity_max:
            return f"{self.capacity_min} student{'s' if self.capacity_min > 1 else ''} per room"
        return f"{self.capacity_min}-{self.capacity_max} students per room"
    
    @property
    def price_display(self):
        """Return formatted price display."""
        return f"${self.price}/{self.period}"
    
    @property
    def main_image_url(self):
        """Return the main image URL."""
        if self.main_image:
            return self.main_image.url
        return None
    
    @property
    def amenity_list(self):
        """Return amenities as a list."""
        return self.amenities or []
    
    @property
    def feature_list(self):
        """Return features as a list."""
        return self.features or []
    
    @property
    def highlight_list(self):
        """Return highlights as a list."""
        return self.highlights or []


class AccommodationReview(models.Model):
    """Reviews for accommodations."""
    
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(TASUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accommodation_reviews'
        verbose_name = 'Accommodation Review'
        verbose_name_plural = 'Accommodation Reviews'
        ordering = ['-created_at']
        unique_together = ['accommodation', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.accommodation.name} ({self.rating} stars)"


class AccommodationInquiry(models.Model):
    """Inquiries about accommodations."""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('viewing_scheduled', 'Viewing Scheduled'),
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('closed', 'Closed'),
    ]
    
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(TASUser, on_delete=models.CASCADE, null=True, blank=True)
    
    # Contact Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Inquiry Details
    message = models.TextField()
    preferred_contact_method = models.CharField(max_length=20, default='email', choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('both', 'Both'),
    ])
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    is_urgent = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contacted_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'accommodation_inquiries'
        verbose_name = 'Accommodation Inquiry'
        verbose_name_plural = 'Accommodation Inquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.accommodation.name}"


class ContactMessage(models.Model):
    """Contact form messages from website visitors."""
    
    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('admissions', 'Admissions'),
        ('academic', 'Academic Programs'),
        ('support', 'Technical Support'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    # Contact Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Message Details
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    is_urgent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    
    # Optional: Link to user if they have an account
    user = models.ForeignKey(TASUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_messages')
    
    class Meta:
        db_table = 'contact_messages'
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_inquiry_type_display()})"
    
    def mark_as_read(self):
        """Mark message as read."""
        self.is_read = True
        self.status = 'read'
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'status', 'read_at'])
    
    def mark_as_replied(self):
        """Mark message as replied."""
        self.status = 'replied'
        self.replied_at = timezone.now()
        self.save(update_fields=['status', 'replied_at'])
    
    @property
    def inquiry_type_display(self):
        """Get the display name for inquiry type."""
        return dict(self.INQUIRY_TYPE_CHOICES).get(self.inquiry_type, self.inquiry_type)
    
    @property
    def status_display(self):
        """Get the display name for status."""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


# Student Registration Model
class Student(models.Model):
    """Student registration model for TAS School Management System."""
    
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('primary', 'Primary School'),
        ('jhs', 'Junior High School'),
        ('shs', 'Senior High School'),
        ('diploma', 'Diploma'),
        ('degree', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('enrolled', 'Enrolled'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    hometown = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    occupation = models.BooleanField(default=False, help_text="Currently employed?")
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    email_address = models.EmailField(unique=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    telephone_number = models.CharField(max_length=20)
    
    # Guarantor Information
    guarantee_name = models.CharField(max_length=100)
    guarantee_number = models.CharField(max_length=20)
    
    # Photo Uploads
    student_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True, help_text="Upload student photo")
    valid_card_photo = models.ImageField(upload_to='student_cards/', blank=True, null=True, help_text="Upload photo of valid ID card")
    
    # Registration Details
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Additional Information
    notes = models.TextField(blank=True, null=True, help_text="Additional notes or comments")
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(TASUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_students')
    
    class Meta:
        db_table = 'students'
        verbose_name = 'Student Registration'
        verbose_name_plural = 'Student Registrations'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.student_id:
            return f"{self.first_name} {self.last_name} ({self.student_id})"
        return f"{self.first_name} {self.last_name} (Pending)"
    
    def save(self, *args, **kwargs):
        # Auto-generate student ID if not provided
        if not self.student_id:
            # Generate student ID in format: STU + year + 6-digit number
            from django.utils import timezone
            year = timezone.now().year
            last_student = Student.objects.filter(
                student_id__startswith=f'STU{year}'
            ).order_by('-student_id').first()
            
            if last_student and last_student.student_id:
                last_number = int(last_student.student_id[-6:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.student_id = f'STU{year}{new_number:06d}'
        
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        """Return full name of the student."""
        first = self.first_name or ''
        last = self.last_name or ''
        return f"{first} {last}".strip() or 'Unnamed Student'
    
    @property
    def student_photo_url(self):
        """Return the student photo URL."""
        if self.student_photo:
            return self.student_photo.url
        return None
    
    @property
    def valid_card_photo_url(self):
        """Return the valid card photo URL."""
        if self.valid_card_photo:
            return self.valid_card_photo.url
        return None
    
    @property
    def status_display(self):
        """Get the display name for status."""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    @property
    def sex_display(self):
        """Get the display name for sex."""
        return dict(self.SEX_CHOICES).get(self.sex, self.sex)
    
    @property
    def marital_status_display(self):
        """Get the display name for marital status."""
        return dict(self.MARITAL_STATUS_CHOICES).get(self.marital_status, self.marital_status)
    
    @property
    def education_level_display(self):
        """Get the display name for education level."""
        return dict(self.EDUCATION_LEVEL_CHOICES).get(self.education_level, self.education_level)


