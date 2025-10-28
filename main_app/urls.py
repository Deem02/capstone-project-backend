from django.urls import path
from .views import DepartmentList, DepartmentDetail

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('departments/',DepartmentList.as_view(),name='department_list'),
    path('departments/<int:department_id>/',DepartmentDetail.as_view(),name='department_detail'),
       path('login/', TokenObtainPairView.as_view(), name='login'),
       path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
    