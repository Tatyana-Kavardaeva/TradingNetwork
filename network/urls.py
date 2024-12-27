from rest_framework.routers import SimpleRouter

from network.apps import NetworkConfig
from network.views import CompanyViewSet

app_name = NetworkConfig.name

router = SimpleRouter()
router.register('companies', CompanyViewSet)

urlpatterns = [] + router.urls
