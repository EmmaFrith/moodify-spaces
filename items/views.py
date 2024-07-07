from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from .models import Item
from .serializers.common import ItemSerializer



class ItemListView(APIView):

  def get(self, _request):
    items = Item.objects.all()
    serialized_item = ItemSerializer(items, many=True)
    return Response(serialized_items.data, status=status.HTTP_200_OK)

    