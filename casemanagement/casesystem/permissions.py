from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class CasePermissions(DjangoModelPermissionsOrAnonReadOnly):
    authenticated_users_only = True
