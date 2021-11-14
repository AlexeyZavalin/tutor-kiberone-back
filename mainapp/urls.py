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
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('groups/<int:group_id>', views.StudentListView.as_view(),
         name='student-list'),
    path('remove-group/', views.RemoveGroup.as_view(), name='remove-group'),
    path('create-group/', views.CreateGroupView.as_view(),
         name='create-group'),
    path('update-group/<int:pk>/', views.UpdateGroupView.as_view(), name='update-group'),
    path('create-student/<int:group_id>', views.CreateStudentView.as_view(),
         name='create-student'),
    path('remove-student/', views.RemoveStudentView.as_view(),
         name='remove-student'),
    path('bulk-update-students/<int:group_id>/', views.bulk_update_students,
         name='bulk-update-students'),
    path('update-student/<int:pk>/', views.UpdateStudentView.as_view(), name='update-student'),
    path('add-custom-kiberons/<int:group_id>',
         views.CreateCustomKiberonRegView.as_view(),
         name='add-custom-kiberons'),
    path('remove-custom-kiberons/<int:group_id>',
         views.RemoveCustomKiberonRegView.as_view(),
         name='remove-custom-kiberons'),
    path('kiberon-log/', views.KiberonLogList.as_view(), name='kiberon-log'),
    path('kiberon-log-search/', views.search_reg, name='kiberon-log-search'),
    path('kiberon-reg-delete/', views.KiberonRegDelete.as_view(), name='kiberon-reg-delete'),
    # path('api-auth/', include('rest_framework.urls',
    # namespace='rest_framework'))
]
