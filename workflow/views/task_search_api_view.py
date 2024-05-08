from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import pagination

from haystack.query import SearchQuerySet

from ..models import Task
from ..api.serializers import TaskSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskSearchAPIView(APIView):
    """
    Fixme: Testing is required..especially using SearchQuerySet with solr..
    """

    def get(self, request, format=None):
        # query = request.GET.get('q', '')
        # search_results = SearchQuerySet().models(Task).filter(content=query)
        # paginator = CustomPagination()
        # paginated_search_results = paginator.paginate_queryset(search_results, request)
        # serializer = TaskSerializer(paginated_search_results, many=True)

        # return Response(serializer.data)
        return null
