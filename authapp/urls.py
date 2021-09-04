from django.urls import path

from authapp import views

app_name = 'authapp'

urlpatterns = [
    path('login/', views.LoginTutor.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.TutorPasswordChangeView.as_view(), name='password-change')
]
