from rest_framework import serializers
from .models import Vote, Employee
from UserAuth.serializers import UserSerializer, ProfileSerializer


class EmployeeSerializer(ProfileSerializer):
    user = UserSerializer()
    company = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=255)

    class Meta(ProfileSerializer.Meta):
        model = Employee
        fields = ProfileSerializer.Meta.fields + ['user', 'is_employee', 'company', 'department']
        read_only_fields = ['id', 'is_employee']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        company = validated_data.pop('company', '')
        department = validated_data.pop('department', '')
        user_data.pop('is_staff', None)
        user_data.pop('is_superuser', None)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            employee = Employee.objects.create(user=user, is_employee=True, is_restaurant_owner=False,
                                               company=company, department=department)
            return employee
        else:
            raise serializers.ValidationError(user_serializer.errors)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['employee', 'menu', 'points', 'created_at']
        read_only_fields = ['created_at', 'employee', 'points']

    def validate_points(self, value):
        if value < 1 or value > 3:
            raise serializers.ValidationError("Points must be between 1 and 3")
        return value
