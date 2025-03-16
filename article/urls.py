from django.urls import path
from .views import dataList

urlpatterns = [
    path('data', dataList.as_view(), name='data-list')
]
