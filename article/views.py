from rest_framework.views import APIView
from .models import Article
from rest_framework.pagination import PageNumberPagination
from .serializers import ArticleSerializer



class CustomPagination(PageNumberPagination):
    page_size = 10  # Adjust as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

class dataList(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('created_at')  # Sorting by created_at descending
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)