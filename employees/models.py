from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class EmployeeManager(BaseUserManager):
    def create_hr(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        hr = self.model(email=email, name=name, is_staff=True, **extra_fields)
        hr.set_password(password)
        hr.save(using=self._db)
        return hr

    def create_employee(self, email, name, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        employee = self.model(email=email, name=name, **extra_fields)
        employee.save(using=self._db)
        return employee

class Employee(AbstractBaseUser):
    """
    This overrides the user model of django with a custom model manager
    """
    HR = 'HR'
    EMPLOYEE = 'EMPLOYEE'
    
    GROUP_CHOICES = [
        (HR, 'HR'),
        (EMPLOYEE, 'Employee'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=10, choices=GROUP_CHOICES, default=EMPLOYEE)
    
    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Attendance(models.Model):
    """
    A model to record attendances for employees
    """
    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("employee", "date")  # Prevent duplicate attendance entries for the same day
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"