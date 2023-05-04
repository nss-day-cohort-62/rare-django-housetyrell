import json
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('id', 'label')

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'label']

class CategoryView(ViewSet):
    """category view class"""
    def list(self, request):
        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)

    def retrieve(self, response, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serialized = CategorySerializer(category, many=False)
            return Response(serialized.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # category = Category()
        serialized = CreateCategorySerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)