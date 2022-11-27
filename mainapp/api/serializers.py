from rest_framework import serializers

from authapp.models import Tutor

from mainapp.models import Group, Student, Kiberon, KiberonStudentReg


class GroupSerializer(serializers.ModelSerializer):
    students_amount = serializers.IntegerField(source='get_students_amount',
                                               read_only=True)

    class Meta:
        model = Group
        exclude = ['is_deleted']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['day_of_week'] = instance.get_day_of_week_display()
        rep['time'] = instance.get_time_display()
        rep['location'] = instance.available_location
        return rep


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['is_deleted']


class KiberonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiberon
        fields = ['achievement', 'value']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['achievement'] = instance.get_achievement_display()
        return rep


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['first_name', 'last_name']


class KiberonStudentRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = KiberonStudentReg
        fields = '__all__'
