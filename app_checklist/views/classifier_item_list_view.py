from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_checklist.models import ClassifierItem

from app_checklist.api.serializers import ClassifierItemSerializer


class ClassifierItemListView(APIView):

    def get(self, request):
        queryset = ClassifierItem.objects.filter(
            code=request.GET.get('code'),  process=request.GET.get('process'))
        serializer = ClassifierItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClassifierItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
