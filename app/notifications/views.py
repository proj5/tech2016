from rest_framework import permissions, status, views
from rest_framework.response import Response

from notifications.models import Read
from notifications.serializers import ReadSerializer


# Create your views here.

class ReadView(views.APIView):

    def get_permissions(self):
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        startID = 999999999
        count = 5
        if request.GET.get('startID') is not None:
            startID = int(request.GET.get('startID'))

        if request.GET.get('count') is not None:
            count = int(request.GET.get('count'))
        # Get 'count' answers of question from startID

        reads = Read.objects.filter(
            user__user=request.user,
            id__lt=startID
        ).order_by('-id').select_related('notification')[:count]

        serializer = ReadSerializer(reads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        if request.GET.get('readID') is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        readID = int(request.GET.get('readID'))
        read = Read.objects.get(pk=readID)
        if not read.read:
            read.read = True
            read.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
