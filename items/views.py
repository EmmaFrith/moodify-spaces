from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from .models import Item
from .serializers.common import ItemSerializer



class ItemListView(APIView):

    def get(self, _request):
        items = Item.objects.all()
        serialized_items = ItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        item_to_add = ItemSerializer(data=request.data)
        try:
            item_to_add.is_valid()
            item_to_add.save()
            return Response(item_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('ERROR')
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)  