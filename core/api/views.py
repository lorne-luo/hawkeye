from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

class BatchDeleteViewSetMixin(object):
    """ provide batch delete endpoints, use with DRF ModelViewSet """

    @list_route(methods=['post', 'delete'])
    def delete(self, request, pk=None):
        """ batch delete, post ids string '1,2,3' to /delete """
        pk = request.POST.get('pk')
        pk = pk.split(',')
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(pk__in=pk)
        if queryset.count():
            queryset.delete()
        else:
            data = {'detail': 'Object not found, or permission denied.'}
            return Response(data, status=404)
        return Response({'success': True}, status=200)
