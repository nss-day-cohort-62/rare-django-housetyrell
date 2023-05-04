import json
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Reaction

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
class CreateReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'label', 'image_url']

class ReactionView(ViewSet):
    """reaction view"""
    def list(self, request):
        reactions = Reaction.objects.all()
        serialized = ReactionSerializer(reactions, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)
            serialized = ReactionSerializer(reaction, many=False)
            return Response(serialized.data)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serialized = CreateReactionSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)