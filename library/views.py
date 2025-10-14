from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book, User, Checkout
from .serializers import BookSerializer, UserSerializer, CheckoutSerializer

# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'isbn']

    # show only available books if ?available=true
    def get_queryset(self):
    # Start with all books
        queryset = Book.objects.all()
    
    # Check if the URL has ?available=true
        available = self.request.query_params.get('available')
        if available == 'true':
        # Filter books where number of copies > borrowed copies
            queryset = [book for book in queryset if book.number_of_copies > book.checkout_set.filter(return_date__isnull=True).count()]
    
        return queryset


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  

# Checkout ViewSet
class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]  

    # Custom action to return a book
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        checkout = self.get_object()
        if checkout.return_date:
            return Response({"error": "Book already returned"})
        checkout.return_date = timezone.now()
        checkout.save()
        return Response({"success": "Book returned"})
