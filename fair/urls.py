from django.urls import path
from fair import views

app_name = 'fair'

urlpatterns = [
    path('souvenirs/', views.souvenirs_list, name='souvenirs'),
    path('fair_create/', views.FairRegistrationCreateView.as_view(),
         name='create_fair_register'),
]
