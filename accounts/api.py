from rest_framework import routers

from accounts.views import UserViewSet, RegisterViewSet

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='custom-users')
router.register(r'register', RegisterViewSet, basename='register')