"""
URL configuration for emsbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from employee.views import EmpGetList, EmpCreate,EmpUpdate,EmpDelete
from attendance.views import CheckIn,CheckOut,GetAllAttendance,GetYourAttendance
from leave.views import CreateLeave,UpdateLeave,SeeLeaves,SeeYourLeave
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('allemployees/', EmpGetList.as_view(), name='All employees'),
    path('employee/create/', EmpCreate.as_view(), name='Create Employee'),
    path('employee/update/<int:pk>/', EmpUpdate.as_view(), name='Update Employee'),
    path('employee/delete/<int:pk>/', EmpDelete.as_view(), name='Delete Employee'),
    path('attendance/checkin/', CheckIn.as_view(), name='checkin Employee'),
    path('attendance/checkout/', CheckOut.as_view(), name='checkout Employee'),
    path('attendance/allAttendance/', GetAllAttendance.as_view(), name='All Attendance'),
    path('attendance/EmpAttendance/', GetYourAttendance.as_view(), name='Employee Attendance'),
]
