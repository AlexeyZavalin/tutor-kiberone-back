from django.urls import path

from test import views

app_name = 'test'

urlpatterns = [
    path('tests/<int:test_id>', views.TestView.as_view(), name='test'),
    path('tests/', views.TestListView.as_view(), name='test-list'),
    path('test-results/<int:pk>',
         views.TestResultDetailView.as_view(), name='test-result'),
    path('test-results/', views.TestResultListView.as_view(),
         name='test-result-list')
]
