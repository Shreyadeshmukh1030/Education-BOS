from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.people.api_views import LearnerViewSet

router = DefaultRouter()
router.register(r'people/learners', LearnerViewSet, basename='learners')

urlpatterns = [
    path('', include(router.urls)),
]
