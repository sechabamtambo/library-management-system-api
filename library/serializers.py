from rest_framework import serializers
from .models import Book, User, Checkout
from django.utils import timezone

# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'number_of_copies']
    # Simple check: ISBN must be 13 digits
    def validate_isbn(self, value):
        if not value.isdigit() or len(value) != 13:
            raise serializers.ValidationError("ISBN must be exactly 13 digits.")
        return value
        
    def validate_published_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return value

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_of_membership', 'is_active']
        
# Checkout Serializer

class CheckoutSerializer(serializers.ModelSerializer):

    def validate(self, data):
        user = data.get('user')
        book = data.get('book')
        checkout_date = data.get('checkout_date')
        return_date = data.get('return_date')

        # User must be active
        if not user.is_active:
            raise serializers.ValidationError("Inactive users cannot borrow books")

        # Return date validation
        if return_date <= checkout_date:
            raise serializers.ValidationError("Return date must be after checkout date.")
        if return_date <= timezone.now():
            raise serializers.ValidationError("Return date must be a future date")
        # checkout_validation
        if checkout_date < timezone.now().date():
            raise serializers.ValidationError("Checkout date cannot be in the past.")


        # Check available copies
        total_copies = book.number_of_copies
        borrowed_count = Checkout.objects.filter(
            book=book,
            return_date__isnull=True
        ).count()
        available_copies = total_copies - borrowed_count
        if available_copies <= 0:
            raise serializers.ValidationError("No available copies for this book")

        return data

    class Meta:
        model = Checkout
        fields = ['id', 'user', 'book', 'checkout_date', 'return_date']

            
            
            
            
