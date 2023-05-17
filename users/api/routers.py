from rest_framework import routers
from .views import UserCreateView, UserGetView

router = routers.SimpleRouter()
router.register('signup', UserCreateView, basename='api-user-signup')
router.register('', UserGetView, basename='api-account')