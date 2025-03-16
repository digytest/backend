from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer



class dataList(APIView):
    

    def get(self, request, *args, **kwargs):
        profiles = Article.objects.all().values()[:20]
        serializer = ArticleSerializer(profiles, many=True)
        return Response(serializer.data)
