from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Article, Category
from rest_framework.pagination import PageNumberPagination
from .serializers import ArticleSerializer, CategorySerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timesince import timesince
class LoginView(ObtainAuthToken):
    
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)
    
class ArticleListCreateView(generics.ListCreateAPIView):
    
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Article.objects.all()
        if self.request.method == "GET":
            queryset = queryset.order_by("-created_at") 

            data = [
            {
                "id": article.id,
                "title": article.title,
                "link": article.link,
                "category_image_url": article.category_image_url,
                "category_id": article.category_id,
                "created_at": timesince(article.created_at) + " ago",
            }
            for article in queryset
        ]
             # Sort by created_at descending
        return data

class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """Allow updating a single field or multiple fields while keeping others unchanged."""
        article = self.get_object()
        data = request.data.copy()

        # Merge existing fields if they are not provided
        if "title" not in data:
            data["title"] = article.title
        if "link" not in data:
            data["link"] = article.link

        serializer = self.get_serializer(article, data=data, partial=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomPagination(PageNumberPagination):
    
    page_size = 5  # Adjust as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

class dataList(APIView):
    
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-created_at')  # Sorting by created_at descending
        
        data = [
            {
                "id": article.id,
                "title": article.title,
                "link": article.link,
                "category_image_url": article.category_image_url,
                "category_id": article.category_id,
                "created_at": timesince(article.created_at) + " ago",
            }
            for article in articles
        ]

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(data, request)
        serializer = ArticleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class CategoryView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        images = Category.objects.all()
        serializer = CategorySerializer(images, many=True)
        return Response(serializer.data)    
    
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    