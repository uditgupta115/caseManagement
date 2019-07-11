from rest_framework.routers import DefaultRouter

from casemanagement.casesystem.viewsets import CaseViewSet

router = DefaultRouter()

router.register('case', CaseViewSet, basename='case_v1')
