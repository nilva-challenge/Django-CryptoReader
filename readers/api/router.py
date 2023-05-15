from rest_framework import routers
from .views import AccountViewSet

router = routers.SimpleRouter()
router.register('positions', AccountViewSet, basename='api-positions')