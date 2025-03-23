from django.urls import path
from .views import dataList
from .views import (
    ArticleListCreateView,
    ArticleRetrieveUpdateDestroyView,
    LoginView,
)
urlpatterns = [
    path("articles/", ArticleListCreateView.as_view(), name="article-list"),
    path("articles/<uuid:pk>/", ArticleRetrieveUpdateDestroyView.as_view(), name="article-detail"),
    path("login/", LoginView.as_view(), name="login"),
    path('data/', dataList.as_view(), name='data-list')
]
