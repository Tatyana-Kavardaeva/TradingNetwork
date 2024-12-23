from rest_framework import viewsets

from network.models import Company
from network.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
