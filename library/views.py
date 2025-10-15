from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book, User, Checkout
from .serializers import BookSerializer, UserSerializer, CheckoutSerializer
from django.shortcuts import render
from .models import Book, Checkout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib import messages


# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'isbn']
    
    def get_queryset(self):
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
    
@login_required
def dashboard_view(request):
    # Fetch all books
    books = Book.objects.all()
    # Fetch only checkouts of the logged-in user
    user_checkouts = Checkout.objects.filter(user=request.user)
    
    context = {
        "books": books,
        "checkouts": user_checkouts
    }
    return render(request, "dashboard.html", context)

# SIGNUP VIEW
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # creates the user
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# LOGIN VIEW
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# LOGOUT VIEW
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
