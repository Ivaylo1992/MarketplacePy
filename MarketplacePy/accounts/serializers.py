from rest_framework import serializers

from .models import UserReview


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ['reviewer', 'reviewed_user', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        # Ensure reviewer and reviewed_user are not the same
        if data['reviewer'] == data['reviewed_user']:
            raise serializers.ValidationError("You cannot review yourself.")
        return data
