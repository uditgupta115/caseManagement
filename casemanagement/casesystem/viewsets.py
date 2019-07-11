from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from casemanagement.casesystem.models import Case
from casemanagement.casesystem.permissions import CasePermissions
from casemanagement.casesystem.serializers import CaseSerializer


class GenericModelViewSet(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet
                          ):
    pass


class CaseViewSet(GenericModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    parser_classes = (JSONParser, MultiPartParser)
    # permission_classes = (CasePermissions, )







