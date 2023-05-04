from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser


class RareUserView(ViewSet):
    """Level up users view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """

        rareuser = RareUser.objects.get(pk=pk)
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
        
        


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'full_name')
