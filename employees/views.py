from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import IntegrityError
from .serializers import EmployeeSerializer, CreateEmployeeSerializer, AttendanceSerializer
from .models import Employee, Attendance


class ListEmployeeView(ListAPIView):
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        queryset = Employee.objects.all()
        name = self.request.query_params.get("name")
        group = self.request.query_params.get("group")
        email = self.request.query_params.get("email")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if group:
            queryset = queryset.filter(group=group)
        if email:
            queryset = queryset.filter(email__icontains=email)
        

        return queryset

class CreateEmployeeView(APIView):
    def post(self, request):
        serializer = CreateEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            password = data.get("password", None)
            group = data.get("group")

            try:        
                if group == "HR" and password:
                    employee = Employee.objects.create_hr(**data)
                else:
                    employee = Employee.objects.create_employee(**data)

                return Response(
                    {"message": f"Employee {employee.email} created successfully"},
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response({"message": "Employee with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveEmployeeView(RetrieveAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

class UpdateEmployeeView(APIView):
    def put(self, request, pk, *args, **kwargs):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data with the existing instance
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        
        # Validate and update
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteEmployeeView(DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class AttendanceListView(APIView):
    """
    List all attendance records or create a new one.
    """
    def get(self, request):
        employeeId = request.query_params.get("employeeId")
        date = request.query_params.get("date")
        dateBetween = request.query_params.get("dateBetween")
        stat = request.query_params.get("status")
        attendance_records = Attendance.objects.all()
        if employeeId:
            attendance_records = attendance_records.filter(employee=employeeId)
        if date:
            attendance_records = attendance_records.filter(date=date)
        if dateBetween:
            try: 
                dates = dateBetween.split(",")
                start_date = dates[0]
                end_date = dates[1]
                attendance_records = attendance_records.filter(date__lte=start_date, date__gte=end_date)
            except:
                return Response({"message": "Error in the 'dateBetween' query param."}, status=status.HTTP_400_BAD_REQUEST)
        if stat:
            attendance_records = attendance_records.filter(status=stat)

        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceDetailView(APIView):
    """
    Retrieve, update, or delete a specific attendance record.
    """
    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return None

    def get(self, request, pk):
        attendance = self.get_object(pk)
        if not attendance:
            return Response({"detail": "Attendance not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    def put(self, request, pk):
        attendance = self.get_object(pk)
        if not attendance:
            return Response({"detail": "Attendance not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        attendance = self.get_object(pk)
        if not attendance:
            return Response({"detail": "Attendance not found."}, status=status.HTTP_404_NOT_FOUND)
        attendance.delete()
        return Response({"detail": "Attendance record deleted."}, status=status.HTTP_204_NO_CONTENT)
    
class Ping(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        return Response({"message": "Ping successfull!"}, status=status.HTTP_200_OK)