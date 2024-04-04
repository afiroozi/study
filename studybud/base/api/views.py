from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRouter(request):
    router = [
        'samal','hi','bye'

    ]        
    return Response(router)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
