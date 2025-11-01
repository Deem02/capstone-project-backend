from django.urls import path, include
from .views import DepartmentList, DepartmentDetail, EmployeeRegister,EmployeeDetail, TaskViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('departments/',DepartmentList.as_view(),name='department_list'),
    path('departments/<int:department_id>/',DepartmentDetail.as_view(),name='department_detail'),
    path('employees/',EmployeeRegister.as_view(),name='employees'),
    path('employees/<int:employee_id>/',EmployeeDetail.as_view(),name='employee_detail'),
  
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include(router.urls)),
]
    