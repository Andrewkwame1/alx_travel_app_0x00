from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing, Booking, Review
from .serializers import (
    ListingSerializer, 
    BookingSerializer, 
    BookingCreateSerializer,
    ReviewSerializer
)


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing property listings.
    
    Provides CRUD operations:
    - list: Get all listings
    - create: Create a new listing
    - retrieve: Get a specific listing
    - update: Update a listing
    - partial_update: Partially update a listing
    - destroy: Delete a listing
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'is_available', 'bedrooms', 'bathrooms']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price_per_night', 'created_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """
        Override to set the listing host to the current user.
        """
        serializer.save(host=self.request.user)

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """
        Custom action to retrieve all bookings for a specific listing.
        URL: /api/listings/{id}/bookings/
        """
        listing = self.get_object()
        bookings = listing.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Custom action to get only available listings.
        URL: /api/listings/available/
        """
        available_listings = self.queryset.filter(is_available=True)
        serializer = self.get_serializer(available_listings, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    
    Provides CRUD operations:
    - list: Get all bookings
    - create: Create a new booking
    - retrieve: Get a specific booking
    - update: Update a booking
    - partial_update: Partially update a booking
    - destroy: Delete a booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['listing', 'user', 'status', 'check_in_date', 'check_out_date']
    ordering_fields = ['check_in_date', 'check_out_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optionally restricts the returned bookings to a given user,
        by filtering against a `user` query parameter in the URL.
        """
        queryset = Booking.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(user__username=user)
        return queryset

    def perform_create(self, serializer):
        """
        Override to set the booking user to the current user.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Custom action to cancel a booking.
        URL: /api/bookings/{id}/cancel/
        """
        booking = self.get_object()
        if booking.status == 'cancelled':
            return Response(
                {'detail': 'Booking is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Custom action to confirm a booking.
        URL: /api/bookings/{id}/confirm/
        """
        booking = self.get_object()
        if booking.status == 'confirmed':
            return Response(
                {'detail': 'Booking is already confirmed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """
        Custom action to get bookings for the authenticated user.
        URL: /api/bookings/my_bookings/
        """
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user_bookings = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_bookings, many=True)
        return Response(serializer.data)