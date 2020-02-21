from rest_framework.routers import DefaultRouter

from casemanagement.casesystem.viewsets import CaseViewSet, AuthViewSet

router = DefaultRouter()

router.register('case', CaseViewSet, basename='case_v1')
router.register('user', AuthViewSet, basename='v1')
