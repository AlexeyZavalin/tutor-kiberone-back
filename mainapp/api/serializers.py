from rest_framework import serializers

from mainapp.models import Group, Student, Kiberon, Tutor


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class KiberonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiberon
        fields = '__all__'


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['full_name']
