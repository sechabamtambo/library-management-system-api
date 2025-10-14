from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserViewSet, CheckoutViewSet

router = DefaultRouter()
router.register('books', BookViewSet)
router.register('users', UserViewSet)
router.register('checkouts', CheckoutViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
