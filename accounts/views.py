from django.shortcuts import render
from rest_framework import status, generics, permissions, viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q, Count, Sum, Avg
from django.http import JsonResponse
from .models import (
    TASUser, StaffProfile, GalleryCategory, GalleryImage, GalleryImageLike, 
    GalleryImageView, GALLERY_ICON_CHOICES,
    AccommodationType, Accommodation, AccommodationReview, AccommodationInquiry,
    ACCOMMODATION_ICON_CHOICES, ACCOMMODATION_AMENITY_CHOICES, ContactMessage,
    Student
)
from .serializers import (
    TASUserSerializer, TASUserWithStaffSerializer, TASUserUpdateSerializer, RegisterSerializer, LoginSerializer, 
    ChangePasswordSerializer, StaffProfileSerializer, UserProfileSerializer,
    GalleryCategorySerializer, GalleryImageSerializer, GalleryImageLikeSerializer,
    GalleryImageViewSerializer, GalleryStatsSerializer, IconChoicesSerializer,
    AccommodationTypeSerializer, AccommodationSerializer, AccommodationReviewSerializer,
    AccommodationInquirySerializer, AccommodationStatsSerializer,
    ContactMessageSerializer, ContactMessageCreateSerializer,
    StudentSerializer, StudentCreateSerializer, StudentStatsSerializer
)
from .permissions import (
    IsDjangoAdmin, IsTASUser, IsTASUserOrDjangoAdmin,
    TASUserPermissionMixin, is_django_admin, is_tas_user,
    IsStaff, IsStaffOrDjangoAdmin, StaffPermissionMixin,
    can_manage_students, can_manage_instructors, can_manage_reports, can_assign_instructors,
    IsStudent, IsStudentOrInstructorOrStaffOrDjangoAdmin
)

TASUser = get_user_model()

def index(request):
    return render(request, 'index.html')
    #return JsonResponse({'message': 'Welcome to the TAS School Management System API'})


class RegisterView(generics.CreateAPIView):
    """View for TAS user registration."""
    
    queryset = TASUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': TASUserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': f'Successfully registered as {user.get_user_type_display()}'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """View for user login (supports both Django admin and TAS users)."""
    
    
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", request.data)
        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", user)
        login(request, user)
        
        refresh = RefreshToken.for_user(user)
        
        # Determine user type for response
        if user.is_superuser:
            user_type = "Django Superuser"
        else:
            user_type = user.get_user_type_display()
        
        return Response({
            'user': TASUserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user_type,
        })
    
class LoginView888888(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_type": getattr(user, "user_type", None),
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """View for user logout."""
    
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."})
        except Exception:
            return Response({"message": "Successfully logged out."})


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for user profile."""
    
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """View for changing password."""
    
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({"message": "Password updated successfully."})




class StaffProfileView(generics.RetrieveUpdateAPIView):
    """View for staff profile."""
    
    serializer_class = StaffProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return StaffProfile.objects.get(user=self.request.user)


class AdminStaffProfileView(generics.RetrieveUpdateAPIView):
    """View for admin to manage any staff profile."""
    
    serializer_class = StaffProfileSerializer
    permission_classes = (IsDjangoAdmin,)
    queryset = StaffProfile.objects.all()
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            return StaffProfile.objects.get(user_id=user_id)
        except StaffProfile.DoesNotExist:
            # Create staff profile if it doesn't exist
            user = TASUser.objects.get(id=user_id)
            return StaffProfile.objects.create(
                user=user,
                staff_id=f"STA{user.id:06d}"
            )




class UserListView(generics.ListAPIView):
    """View for listing users (admin only)."""
    
    serializer_class = TASUserWithStaffSerializer
    permission_classes = (IsDjangoAdmin,)
    queryset = TASUser.objects.all()
    
    def get_queryset(self):
        queryset = TASUser.objects.all()
        user_type = self.request.query_params.get('user_type', None)
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for user detail (admin only)."""
    
    permission_classes = (IsDjangoAdmin,)
    queryset = TASUser.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TASUserUpdateSerializer
        return TASUserSerializer






@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_types(request):
    """Get available user types."""
    return Response({
        'user_types': [
            {'value': 'staff', 'label': 'Staff'},
        ]
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_info(request):
    """Get current user information."""
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsDjangoAdmin])
def get_system_stats(request):
    """Get system statistics (admin only)."""
    stats = {
        'total_users': TASUser.objects.count(),
        'staff': TASUser.objects.filter(user_type='staff').count(),
        'active_users': TASUser.objects.filter(is_active=True).count(),
    }
    return Response(stats)


# Staff Dashboard Views
@api_view(['GET'])
@permission_classes([IsStaffOrDjangoAdmin])
def get_staff_dashboard_stats(request):
    """Get staff dashboard statistics."""
    stats = {
        'total_staff': TASUser.objects.filter(user_type='staff').count(),
        'active_staff': TASUser.objects.filter(user_type='staff', is_active=True).count(),
        'total_users': TASUser.objects.count(),
    }
    return Response(stats) 

# Gallery Views
class GalleryCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Gallery Categories with full CRUD operations."""
    
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'display_order', 'created_at']
    ordering = ['display_order', 'name']
    
    def get_queryset(self):
        queryset = GalleryCategory.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active categories."""
        categories = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle category active status."""
        category = self.get_object()
        category.is_active = not category.is_active
        category.save()
        return Response({'is_active': category.is_active})


class GalleryImageViewSet(viewsets.ModelViewSet):
    """ViewSet for Gallery Images with full CRUD operations."""
    
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'tags', 'location']
    ordering_fields = ['title', 'created_at', 'views_count', 'likes_count', 'display_order']
    ordering = ['-is_featured', 'display_order', '-created_at']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        queryset = GalleryImage.objects.select_related('category', 'created_by')
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by featured status
        is_featured = self.request.query_params.get('is_featured', None)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        
        # Filter by tags
        tags = self.request.query_params.get('tags', None)
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                queryset = queryset.filter(tags__icontains=tag)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to track views."""
        instance = self.get_object()
        
        # Track view
        if request.user.is_authenticated:
            GalleryImageView.objects.create(
                image=instance,
                user=request.user,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        else:
            GalleryImageView.objects.create(
                image=instance,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        # Increment view count
        instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured images."""
        images = self.queryset.filter(is_featured=True, is_active=True)
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent images."""
        limit = int(request.query_params.get('limit', 10))
        images = self.queryset.filter(is_active=True)[:limit]
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular images (most viewed/liked)."""
        limit = int(request.query_params.get('limit', 10))
        images = self.queryset.filter(is_active=True).order_by('-views_count', '-likes_count')[:limit]
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like/unlike an image."""
        image = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        like, created = GalleryImageLike.objects.get_or_create(image=image, user=user)
        
        if created:
            image.increment_likes()
            return Response({'liked': True, 'likes_count': image.likes_count})
        else:
            like.delete()
            image.likes_count = max(0, image.likes_count - 1)
            image.save(update_fields=['likes_count'])
            return Response({'liked': False, 'likes_count': image.likes_count})
    
    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
        """Toggle image featured status."""
        image = self.get_object()
        image.is_featured = not image.is_featured
        image.save()
        return Response({'is_featured': image.is_featured})
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle image active status."""
        image = self.get_object()
        image.is_active = not image.is_active
        image.save()
        return Response({'is_active': image.is_active})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gallery_stats(request):
    """Get gallery statistics."""
    stats = {
        'total_images': GalleryImage.objects.filter(is_active=True).count(),
        'total_categories': GalleryCategory.objects.filter(is_active=True).count(),
        'total_views': GalleryImage.objects.filter(is_active=True).aggregate(
            total=Sum('views_count'))['total'] or 0,
        'total_likes': GalleryImage.objects.filter(is_active=True).aggregate(
            total=Sum('likes_count'))['total'] or 0,
        'featured_images': GalleryImage.objects.filter(is_featured=True, is_active=True).count(),
        'recent_images': GalleryImage.objects.filter(
            is_active=True,
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
        ).count(),
        'popular_categories': list(
            GalleryCategory.objects.filter(is_active=True)
            .annotate(image_count=Count('images'))
            .filter(image_count__gt=0)
            .order_by('-image_count')[:5]
            .values('name', 'image_count')
        ),
        'recent_activity': list(
            GalleryImage.objects.filter(is_active=True)
            .order_by('-created_at')[:10]
            .values('title', 'created_at', 'category__name')
        )
    }
    
    serializer = GalleryStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gallery_icon_choices(request):
    """Get available icon choices for gallery categories."""
    choices = [{'value': choice[0], 'label': choice[1]} for choice in GALLERY_ICON_CHOICES]
    return Response({'icon_choices': choices})


""" @api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gallery_categories(request):
    Get all active gallery categories with image counts.
    categories = GalleryCategory.objects.filter(is_active=True).annotate(
        image_count=Count('images', filter=Q(images__is_active=True))
    ).order_by('display_order', 'name')
    
    serializer = GalleryCategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)
 """

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gallery_categories(request):
    """Get all active gallery categories with image counts."""
    categories = GalleryCategory.objects.filter(is_active=True).order_by('display_order', 'name')
    serializer = GalleryCategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gallery_images(request):
    """Get gallery images with filtering options."""
    images = GalleryImage.objects.filter(is_active=True).select_related('category', 'created_by')
    
    # Filter by category
    category = request.GET.get('category')
    if category and category != 'all':
        images = images.filter(category__slug=category)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        images = images.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(tags__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Ordering
    order_by = request.GET.get('order_by', '-created_at')
    if order_by in ['title', '-title', 'created_at', '-created_at', 'views_count', '-views_count', 'likes_count', '-likes_count']:
        images = images.order_by(order_by)
    else:
        images = images.order_by('-is_featured', 'display_order', '-created_at')
    
    # Pagination
    limit = int(request.GET.get('limit', 24))
    offset = int(request.GET.get('offset', 0))
    total_count = images.count()
    images = images[offset:offset + limit]
    
    serializer = GalleryImageSerializer(images, many=True, context={'request': request})
    
    return Response({
        'results': serializer.data,
        'count': total_count,
        'next': offset + limit < total_count,
        'previous': offset > 0
    }) 

# Accommodation Views
class AccommodationTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for AccommodationType CRUD operations."""
    
    queryset = AccommodationType.objects.all()
    serializer_class = AccommodationTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'display_order', 'created_at']
    ordering = ['display_order', 'name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('active_only') == 'true':
            queryset = queryset.filter(is_active=True)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()


class AccommodationViewSet(viewsets.ModelViewSet):
    """ViewSet for Accommodation CRUD operations."""
    
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['name', 'price', 'rating', 'created_at', 'display_order']
    ordering = ['-is_featured', 'display_order', 'name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by accommodation type
        accommodation_type = self.request.query_params.get('type')
        if accommodation_type:
            queryset = queryset.filter(accommodation_type__slug=accommodation_type)
        
        # Filter by availability
        availability = self.request.query_params.get('availability')
        if availability:
            queryset = queryset.filter(availability=availability)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        
        # Filter active only
        if self.request.query_params.get('active_only') == 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()


class AccommodationReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for AccommodationReview CRUD operations."""
    
    queryset = AccommodationReview.objects.all()
    serializer_class = AccommodationReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by accommodation
        accommodation_id = self.request.query_params.get('accommodation')
        if accommodation_id:
            queryset = queryset.filter(accommodation_id=accommodation_id)
        
        # Filter approved reviews only for public access
        if self.request.query_params.get('approved_only') == 'true':
            queryset = queryset.filter(is_approved=True)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccommodationInquiryViewSet(viewsets.ModelViewSet):
    """ViewSet for AccommodationInquiry CRUD operations."""
    
    queryset = AccommodationInquiry.objects.all()
    serializer_class = AccommodationInquirySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by accommodation
        accommodation_id = self.request.query_params.get('accommodation')
        if accommodation_id:
            queryset = queryset.filter(accommodation_id=accommodation_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Users can only see their own inquiries unless they're staff/admin
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_accommodation_stats(request):
    """Get accommodation statistics."""
    try:
        stats = {
            'total_accommodations': Accommodation.objects.filter(is_active=True).count(),
            'total_types': AccommodationType.objects.filter(is_active=True).count(),
            'total_reviews': AccommodationReview.objects.filter(is_approved=True).count(),
            'total_inquiries': AccommodationInquiry.objects.count(),
            'average_rating': Accommodation.objects.filter(is_active=True).aggregate(
                avg_rating=Avg('rating')
            )['avg_rating'] or 0,
            'featured_accommodations': Accommodation.objects.filter(is_featured=True, is_active=True).count(),
            'available_accommodations': Accommodation.objects.filter(availability='available', is_active=True).count(),
            'popular_types': [],
            'recent_accommodations': []
        }
        
        # Popular types
        popular_types = AccommodationType.objects.annotate(
            accommodation_count=Count('accommodations', filter=Q(accommodations__is_active=True))
        ).filter(accommodation_count__gt=0).order_by('-accommodation_count')[:5]
        
        stats['popular_types'] = [
            {
                'name': type_obj.name,
                'count': type_obj.accommodation_count,
                'icon': type_obj.icon,
                'color': type_obj.color
            }
            for type_obj in popular_types
        ]
        
        # Recent accommodations
        recent_accommodations = Accommodation.objects.filter(is_active=True).order_by('-created_at')[:5]
        stats['recent_accommodations'] = [
            {
                'id': acc.id,
                'name': acc.name,
                'type': acc.accommodation_type.name,
                'price': float(acc.price),
                'rating': float(acc.rating),
                'image_url': acc.main_image_url
            }
            for acc in recent_accommodations
        ]
        
        return Response(stats)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_accommodation_icon_choices(request):
    """Get available icon choices for accommodation types."""
    choices = [{'value': choice[0], 'label': choice[1]} for choice in ACCOMMODATION_ICON_CHOICES]
    return Response({'icon_choices': choices})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_accommodation_amenity_choices(request):
    """Get available amenity choices for accommodations."""
    choices = [{'value': choice[0], 'label': choice[1]} for choice in ACCOMMODATION_AMENITY_CHOICES]
    return Response({'amenity_choices': choices})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_accommodation_types(request):
    """Get filtered list of accommodation types."""
    types = AccommodationType.objects.filter(is_active=True)
    
    # Search
    search = request.GET.get('search')
    if search:
        types = types.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Ordering
    order_by = request.GET.get('order_by', 'display_order')
    if order_by in ['name', '-name', 'display_order', '-display_order', 'created_at', '-created_at']:
        types = types.order_by(order_by)
    else:
        types = types.order_by('display_order', 'name')
    
    serializer = AccommodationTypeSerializer(types, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_accommodations(request):
    """Get filtered list of accommodations."""
    accommodations = Accommodation.objects.filter(is_active=True)
    
    # Search
    search = request.GET.get('search')
    if search:
        accommodations = accommodations.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Filter by type
    accommodation_type = request.GET.get('type')
    if accommodation_type:
        accommodations = accommodations.filter(accommodation_type__slug=accommodation_type)
    
    # Filter by availability
    availability = request.GET.get('availability')
    if availability:
        accommodations = accommodations.filter(availability=availability)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        accommodations = accommodations.filter(price__gte=min_price)
    if max_price:
        accommodations = accommodations.filter(price__lte=max_price)
    
    # Filter by rating
    min_rating = request.GET.get('min_rating')
    if min_rating:
        accommodations = accommodations.filter(rating__gte=min_rating)
    
    # Ordering
    order_by = request.GET.get('order_by', '-is_featured')
    if order_by in ['name', '-name', 'price', '-price', 'rating', '-rating', 'created_at', '-created_at']:
        accommodations = accommodations.order_by(order_by)
    else:
        accommodations = accommodations.order_by('-is_featured', 'display_order', 'name')
    
    # Pagination
    limit = int(request.GET.get('limit', 12))
    offset = int(request.GET.get('offset', 0))
    total_count = accommodations.count()
    accommodations = accommodations[offset:offset + limit]
    
    serializer = AccommodationSerializer(accommodations, many=True, context={'request': request})
    
    return Response({
        'results': serializer.data,
        'count': total_count,
        'next': offset + limit < total_count,
        'previous': offset > 0
    })


# Contact Message Views
class ContactMessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing contact messages."""
    
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrDjangoAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at', 'updated_at', 'name', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactMessageCreateSerializer
        return ContactMessageSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]  # Allow public contact form submission
        else:
            permission_classes = [permissions.IsAuthenticated, IsStaffOrDjangoAdmin]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Create a new contact message."""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        contact_message = serializer.save()
        
        # Return success response
        return Response({
            'message': 'Contact message sent successfully!',
            'data': ContactMessageSerializer(contact_message, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a contact message as read."""
        contact_message = self.get_object()
        contact_message.mark_as_read()
        return Response({'message': 'Message marked as read'})
    
    @action(detail=True, methods=['post'])
    def mark_as_replied(self, request, pk=None):
        """Mark a contact message as replied."""
        contact_message = self.get_object()
        contact_message.mark_as_replied()
        return Response({'message': 'Message marked as replied'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get contact message statistics."""
        total_messages = ContactMessage.objects.count()
        new_messages = ContactMessage.objects.filter(status='new').count()
        read_messages = ContactMessage.objects.filter(is_read=True).count()
        replied_messages = ContactMessage.objects.filter(status='replied').count()
        urgent_messages = ContactMessage.objects.filter(is_urgent=True).count()
        
        # Messages by inquiry type
        inquiry_stats = ContactMessage.objects.values('inquiry_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Recent messages (last 7 days)
        week_ago = timezone.now() - timezone.timedelta(days=7)
        recent_messages = ContactMessage.objects.filter(created_at__gte=week_ago).count()
        
        return Response({
            'total_messages': total_messages,
            'new_messages': new_messages,
            'read_messages': read_messages,
            'replied_messages': replied_messages,
            'urgent_messages': urgent_messages,
            'recent_messages': recent_messages,
            'inquiry_stats': inquiry_stats
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def submit_contact_message(request):
    """Public endpoint for submitting contact messages."""
    serializer = ContactMessageCreateSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        contact_message = serializer.save()
        return Response({
            'success': True,
            'message': 'Thank you for your message! We will get back to you within 24 hours.',
            'data': {
                'id': contact_message.id,
                'name': contact_message.name,
                'subject': contact_message.subject,
                'created_at': contact_message.created_at
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'There was an error submitting your message. Please try again.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# Student Views
class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student CRUD operations."""
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrDjangoAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email_address', 'student_id', 'hometown', 'guarantee_name']
    ordering_fields = ['first_name', 'last_name', 'registration_date', 'status', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by sex
        sex_filter = self.request.query_params.get('sex')
        if sex_filter:
            queryset = queryset.filter(sex=sex_filter)
        
        # Filter by education level
        education_filter = self.request.query_params.get('education_level')
        if education_filter:
            queryset = queryset.filter(education_level=education_filter)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by occupation
        occupation = self.request.query_params.get('occupation')
        if occupation is not None:
            queryset = queryset.filter(occupation=occupation.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a student registration."""
        student = self.get_object()
        student.status = 'approved'
        student.save()
        return Response({'message': 'Student approved successfully', 'status': student.status})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a student registration."""
        student = self.get_object()
        student.status = 'rejected'
        student.save()
        return Response({'message': 'Student rejected', 'status': student.status})
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll an approved student."""
        student = self.get_object()
        if student.status != 'approved':
            return Response({'error': 'Student must be approved before enrollment'}, status=status.HTTP_400_BAD_REQUEST)
        student.status = 'enrolled'
        student.save()
        return Response({'message': 'Student enrolled successfully', 'status': student.status})
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle student active status."""
        student = self.get_object()
        student.is_active = not student.is_active
        student.save()
        return Response({'is_active': student.is_active})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsStaffOrDjangoAdmin])
def get_student_stats(request):
    """Get student statistics."""
    try:
        # Basic counts
        total_students = Student.objects.count()
        pending_students = Student.objects.filter(status='pending').count()
        approved_students = Student.objects.filter(status='approved').count()
        enrolled_students = Student.objects.filter(status='enrolled').count()
        rejected_students = Student.objects.filter(status='rejected').count()
        active_students = Student.objects.filter(is_active=True).count()
        
        # Recent registrations (last 30 days)
        month_ago = timezone.now() - timezone.timedelta(days=30)
        recent_registrations = Student.objects.filter(created_at__gte=month_ago).count()
        
        # Students by sex
        students_by_sex = Student.objects.values('sex').annotate(count=Count('id'))
        students_by_sex = {item['sex']: item['count'] for item in students_by_sex}
        
        # Students by education level
        students_by_education = Student.objects.values('education_level').annotate(count=Count('id'))
        students_by_education = {item['education_level']: item['count'] for item in students_by_education}
        
        # Students by status
        students_by_status = Student.objects.values('status').annotate(count=Count('id'))
        students_by_status = {item['status']: item['count'] for item in students_by_status}
        
        # Recent students
        recent_students = Student.objects.order_by('-created_at')[:10]
        recent_students_data = [
            {
                'id': student.id,
                'full_name': student.full_name,
                'student_id': student.student_id,
                'email': student.email_address,
                'status': student.status,
                'created_at': student.created_at
            }
            for student in recent_students
        ]
        
        stats = {
            'total_students': total_students,
            'pending_students': pending_students,
            'approved_students': approved_students,
            'enrolled_students': enrolled_students,
            'rejected_students': rejected_students,
            'active_students': active_students,
            'recent_registrations': recent_registrations,
            'students_by_sex': students_by_sex,
            'students_by_education': students_by_education,
            'students_by_status': students_by_status,
            'recent_students': recent_students_data
        }
        
        return Response(stats)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_student_choices(request):
    """Get available choices for student form fields."""
    choices = {
        'sex_choices': [{'value': choice[0], 'label': choice[1]} for choice in Student.SEX_CHOICES],
        'marital_status_choices': [{'value': choice[0], 'label': choice[1]} for choice in Student.MARITAL_STATUS_CHOICES],
        'education_level_choices': [{'value': choice[0], 'label': choice[1]} for choice in Student.EDUCATION_LEVEL_CHOICES],
        'status_choices': [{'value': choice[0], 'label': choice[1]} for choice in Student.STATUS_CHOICES],
    }
    return Response(choices)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsStaffOrDjangoAdmin])
def get_students(request):
    """Get filtered list of students."""
    students = Student.objects.all()
    
    # Search
    search = request.GET.get('search')
    if search:
        students = students.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email_address__icontains=search) |
            Q(student_id__icontains=search) |
            Q(hometown__icontains=search) |
            Q(guarantee_name__icontains=search)
        )
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        students = students.filter(status=status_filter)
    
    # Filter by sex
    sex_filter = request.GET.get('sex')
    if sex_filter:
        students = students.filter(sex=sex_filter)
    
    # Filter by education level
    education_filter = request.GET.get('education_level')
    if education_filter:
        students = students.filter(education_level=education_filter)
    
    # Filter by active status
    is_active = request.GET.get('is_active')
    if is_active is not None:
        students = students.filter(is_active=is_active.lower() == 'true')
    
    # Filter by occupation
    occupation = request.GET.get('occupation')
    if occupation is not None:
        students = students.filter(occupation=occupation.lower() == 'true')
    
    # Ordering
    order_by = request.GET.get('order_by', '-created_at')
    if order_by in ['first_name', '-first_name', 'last_name', '-last_name', 'registration_date', '-registration_date', 'status', '-status', 'created_at', '-created_at']:
        students = students.order_by(order_by)
    else:
        students = students.order_by('-created_at')
    
    # Pagination
    limit = int(request.GET.get('limit', 20))
    offset = int(request.GET.get('offset', 0))
    total_count = students.count()
    students = students[offset:offset + limit]
    
    serializer = StudentSerializer(students, many=True, context={'request': request})
    
    return Response({
        'results': serializer.data,
        'count': total_count,
        'next': offset + limit < total_count,
        'previous': offset > 0
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def submit_student_registration(request):
    """Public endpoint for submitting student registration."""
    serializer = StudentCreateSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        student = serializer.save()
        return Response({
            'success': True,
            'message': 'Student registration submitted successfully! Your application is under review.',
            'data': {
                'id': student.id,
                'full_name': student.full_name,
                'student_id': student.student_id,
                'email': student.email_address,
                'status': student.status,
                'created_at': student.created_at
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'There was an error submitting your registration. Please try again.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST) 