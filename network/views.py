from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from network.models import Company
from network.services import get_company_level
from users.permissions import IsActive
from network.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Company. """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsActive,)
    filterset_fields = ('country',)

    def perform_create(self, serializer):
        """ Устанавливает уровень компании при создании объекта.  """

        supplier_pk = self.request.data.get('supplier')
        supplier = get_object_or_404(Company, pk=supplier_pk) if supplier_pk else None
        company_level = get_company_level(supplier)

        serializer.save(company_level=company_level)

    def perform_update(self, serializer):
        """ Устанавливает уровень компании при обновлении объекта.  """

        supplier_pk = self.request.data.get('supplier')
        supplier = get_object_or_404(Company, pk=supplier_pk) if supplier_pk else None
        new_company_level = get_company_level(supplier)

        serializer.save(company_level=new_company_level)
