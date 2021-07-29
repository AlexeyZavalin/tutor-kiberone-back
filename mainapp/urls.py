from django.urls import include, path
from rest_framework import routers
# from mainapp.api.views import GroupViewSet, StudentViewSet, KiberonViewSet, TutorViewSet, KiberonStudentRegViewSet
from mainapp.views import MainRedirectView, LoginTutor, logout_view, GroupListView, RemoveGroup, GroupDetailView

app_name = 'mainapp'

# router = routers.DefaultRouter()
# router.register(r'groups', GroupViewSet, basename='group')
# router.register(r'students', StudentViewSet, basename='student')
# router.register(r'kiberons', KiberonViewSet, basename='kiberon')
# router.register(r'tutors', TutorViewSet, basename='tutor')
# router.register(r'regs', KiberonStudentRegViewSet, basename='regs')

urlpatterns = [
    path('', MainRedirectView.as_view(), name='main_redirect'),
    path('login/', LoginTutor.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('groups/<int:pk>', GroupDetailView.as_view(), name='group-detail'),
    path('groups/', GroupListView.as_view(), name='groups'),
    path('remove-group/', RemoveGroup.as_view(), name='remove-group')
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
