from django.db import models

# Books model 
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13)
    published_date = models.DateField()
    number_of_copies = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.title

#Users Model    
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_membership = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
# Checkout model    
class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} borrowed the book {self.book}"