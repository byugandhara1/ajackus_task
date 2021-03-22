from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cms import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('api/auth', views.AuthViewSet,basename='api/auth')

urlpatterns = [
    path('', include(router.urls)),
    path('content/',views.UserSearchList.as_view()),
    path('usercontent/',views.ContentView.as_view()),
    path('usercontent/<int:pk>/',views.Contentdetailview.as_view())


]
