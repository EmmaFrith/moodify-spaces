from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers.common import ItemSerializer
from rest_framework.exceptions import NotFound

class ItemListView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        logged_in_user = request.user.id
        items = Item.objects.filter(owner=logged_in_user)
        serialized_items = ItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data["owner"] = request.user.id
        item_to_add = ItemSerializer(data=request.data)
        try:
            item_to_add.is_valid()
            item_to_add.save()
            return Response(item_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('ERROR')
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)  


class ItemDetailView(APIView):

    def get_item(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise NotFound(detail="Can't find that item.")
    
    def get(self, _request, pk):
        item = self.get_item(pk=pk) 
        serialized_item = ItemSerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        item_to_update = self.get_item(pk=pk)
        updated_item = ItemSerializer(item_to_update, data=request.data)
        try:
            updated_item.is_valid()
            updated_item.save()
            return Response(updated_item.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        item_to_delete = self.get_item(pk=pk)
        item_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)