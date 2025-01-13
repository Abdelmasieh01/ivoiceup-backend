from dj_rest_auth.serializers import LoginSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Employee, Attendance

class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        user = self.get_auth_user(attrs)
        if user.group != 'HR':
            raise ValidationError("Only HR employees can access the system.")
        return super().validate(attrs)

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "name", "email", "group", "last_login")

class CreateEmployeeSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    group = serializers.ChoiceField(choices=("HR", "EMPLOYEE"))
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        group = attrs.get("group")
        password = attrs.get("password")

        if group == "EMPLOYEE" and password:
            raise ValidationError("Only HR employees can have passwords.")
        elif group == "HR" and not password:
            raise ValidationError("Password field cannot be empty for HR employees.")

        return attrs

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "employee", "date", "status"]