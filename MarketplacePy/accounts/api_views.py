from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserReviewSerializer


class UserReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['reviewer'] = request.user.pk  # Automatically assign the current user as the reviewer

        # Infer the reviewed_user from the URL or context
        reviewed_user_id = kwargs.get('reviewed_user_id')
        if not reviewed_user_id:
            return Response({'error': 'Reviewed user not specified.'}, status=status.HTTP_400_BAD_REQUEST)

        data['reviewed_user'] = reviewed_user_id
        serializer = UserReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
