import os
import sys
import django
import random
from faker import Faker 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from library.models import Book, User

fake = Faker()

# Create 5 users
for _ in range(5):
    User.objects.create(
        username=fake.user_name(),
        email=fake.email(),
        is_active=True
    )
# Create 10 books
for _ in range(10):
    Book.objects.create(
        title=fake.sentence(nb_words=3),
        author=fake.name(),
        isbn="".join([str(random.randint(0, 9)) for _ in range(13)]),  #
        published_date=fake.date_this_century(),
        number_of_copies=random.randint(1, 5)
    )
    


print("Fake data created successfully!")
