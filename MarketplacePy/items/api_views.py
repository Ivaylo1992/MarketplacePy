from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from MarketplacePy.items.models import ItemLike, Item


class LikeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        item = Item.objects.filter(id=item_id).first()
        if not item:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        liked = ItemLike.objects.filter(item=item, user=request.user).exists()

        if liked:
            # Delete the like
            ItemLike.objects.filter(item=item, user=request.user).delete()
            is_liked = False
        else:
            ItemLike.objects.create(item=item, user=request.user)
            is_liked = True

        return Response({
            'is_liked': is_liked,
            'like_count': item.likes.count()  # Include updated like count
        })
