from django.urls import path
from rest_framework import routers
from .rest import PostViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='Post')
router.register(r'category', CategoryViewSet, basename='Category')

urlpatterns = router.urls
