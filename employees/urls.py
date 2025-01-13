from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path("", views.ListEmployeeView.as_view(), name="employee-list"),
    path("create/", views.CreateEmployeeView.as_view(), name="employee-create"),
    path("<int:pk>/", views.RetrieveEmployeeView.as_view(), name="employee"),   
    path("<int:pk>/update/", views.UpdateEmployeeView.as_view(), name="employee-edit"),
    path("attendance/", views.AttendanceListView.as_view(), name="attendance-list"),
    path("attendance/<int:pk>/", views.AttendanceDetailView.as_view(), name="attendance-detail"),   
    path("ping/", views.Ping.as_view(), name="ping"),
]