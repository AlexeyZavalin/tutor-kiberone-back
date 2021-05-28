from rest_framework import viewsets
from rest_framework import permissions

from mainapp.api.serializers import GroupSerializer, StudentSerializer, KiberonSerializer, TutorSerializer
from mainapp.models import Group, Student, Kiberon, Tutor


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.active.all()
    serializer_class = GroupSerializer
    filterset_fields = ['day_of_week', 'tutor']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.active.all()
    serializer_class = StudentSerializer
    filterset_fields = ['group']
    search_fields = ['name']


class KiberonViewSet(viewsets.ModelViewSet):
    queryset = Kiberon.objects.all()
    serializer_class = KiberonSerializer


class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
