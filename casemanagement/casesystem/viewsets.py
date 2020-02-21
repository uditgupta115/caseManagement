from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from casemanagement.casesystem.models import Case, User
from casemanagement.casesystem.permissions import CasePermissions
from casemanagement.casesystem.serializers import CaseSerializer, UserSerializer


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

    def perform_destroy(self, instance):
        instance.task_set.all().delete()
        instance.delete()


class AuthViewSet(GenericModelViewSet):
    """
    {
        "username": "task1",
        "first_name": "task1",
        "email": "task1@yopmail.com",
        "password": "udit",
        "last_name": "udit",
        "userrole": {"role": 2}
    }

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (JSONParser, MultiPartParser)
    # permission_classes = (CasePermissions, )

    def perform_destroy(self, instance):
        instance.task_set.all().delete()
        instance.delete()





