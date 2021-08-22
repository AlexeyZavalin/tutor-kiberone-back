from django.urls import path
# from rest_framework import routers
# from mainapp.api.views import GroupViewSet, StudentViewSet, KiberonViewSet,
# TutorViewSet,
# KiberonStudentRegViewSet

from mainapp import views

app_name = 'mainapp'

# router = routers.DefaultRouter()
# router.register(r'groups', GroupViewSet, basename='group')
# router.register(r'students', StudentViewSet, basename='student')
# router.register(r'kiberons', KiberonViewSet, basename='kiberon')
# router.register(r'tutors', TutorViewSet, basename='tutor')
# router.register(r'regs', KiberonStudentRegViewSet, basename='regs')

urlpatterns = [
    path('', views.MainRedirectView.as_view(), name='main_redirect'),
    path('groups/<int:pk>', views.GroupDetailView.as_view(),
         name='group-detail'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('remove-group/', views.RemoveGroup.as_view(), name='remove-group'),
    path('create-group/', views.CreateGroupView.as_view(), name='create-group')
    # path('api-auth/', include('rest_framework.urls',
    # namespace='rest_framework'))
]
