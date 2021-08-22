from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from authapp.models import Tutor

from mainapp.api.serializers import GroupSerializer, StudentSerializer, KiberonSerializer, TutorSerializer, \
    KiberonStudentRegSerializer
from mainapp.models import Group, Student, Kiberon, KiberonStudentReg


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name': user.first_name
        })


class KiberonStudentRegPagination(PageNumberPagination):
    page_size = 50
    page_query_param = 'page_size'
    max_page_size = 200


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


class KiberonStudentRegViewSet(viewsets.ModelViewSet):
    queryset = KiberonStudentReg.objects.all()
    serializer_class = KiberonStudentRegSerializer
    pagination_class = KiberonStudentRegPagination
    filterset_fields = ['date']
