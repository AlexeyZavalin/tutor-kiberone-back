from django.urls import include, path
from rest_framework import routers
from mainapp.api.views import GroupViewSet, StudentViewSet, KiberonViewSet, TutorViewSet

app_name = 'mainapp'

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'kiberons', KiberonViewSet, basename='kiberon')
router.register(r'tutors', TutorViewSet, basename='tutor')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
