from django.urls import path

from authapp import views

app_name = 'authapp'

urlpatterns = [
    path('login/', views.LoginTutor.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.TutorPasswordChangeView.as_view(),
         name='password-change'),
    path('student_logout/', views.logout_student, name='student_logout'),
    path('student_login/', views.LoginStudent.as_view(), name='student_login'),
    path('switch_theme/', views.SwitchUserTheme.as_view(), name='switch_theme')
]
