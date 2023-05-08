from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser, Subscription
from rest_framework.decorators import action
from django.db.models import Q, Count
import datetime

class RareUserView(ViewSet):
    """Level up users view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """
        try:
            subscription = Subscription.objects.get(follower_id=request.auth.user.id, author_id=pk)
            rareuser = RareUser.objects.annotate(
                subscribed = Count(
                    "subscribers",
                    filter=Q(subscribers=subscription)
                )
            ).get(pk=pk)
        except Subscription.DoesNotExist:
            rareuser = RareUser.objects.get(pk=pk)
            rareuser.subscribed = 0
        serializer = RareUserSerializer(rareuser)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of users
        """
        rareusers = RareUser.objects.all()
        serializer = RareUserSerializer(rareusers, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized user instance
        """
    @action(methods=['post'], detail=True)       
    def subscribe(self, request, pk):
        author = RareUser.objects.get(pk=pk)
        subscriber = RareUser.objects.get(pk=request.auth.user.id)
        created_on = request.data['created_on']
        subscription = Subscription.objects.create(author=author, follower= subscriber, created_on=created_on)
        return Response({'message': 'Subscribed to User'}, status=status.HTTP_201_CREATED)  
    @action(methods=['delete'], detail=True)
    def unsubscribe(self, request, pk):
        subscription = Subscription.objects.get(author=pk, follower=request.auth.user.id)
        subscription.delete()
        return Response({'message': 'Unsubscribed'}, status=status.HTTP_204_NO_CONTENT)

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'full_name', 'subscribedTo', 'subscribed', 'subscribers')
        depth = 1

