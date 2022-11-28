from django.urls import path

from test import views

app_name = 'test'

urlpatterns = [
    path('tests/<int:test_id>', views.TestView.as_view(), name='test'),
    path('tests/', views.TestListView.as_view(), name='test-list'),
    path('tests-results/<int:test_id>/<int:pk>',
         views.TestResultDetailView.as_view(), name='test-result'),
    path('tests-results/<int:test_id>', views.TestResultListView.as_view(),
         name='test-result-list'),
    path('tests-results/', views.TestResultsListView.as_view(),
         name='tests-result-list'),
]
