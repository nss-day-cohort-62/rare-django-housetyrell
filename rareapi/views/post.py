from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, RareUser, Comment, Subscription, Tag, PostTag
from django.core.exceptions import ValidationError
from rest_framework.decorators import action


class PostView(ViewSet):
    """Level up game types view"""
  
    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
       
        """
        posts = Post.objects.all()
        category_id = request.query_params.get('category', None)
        tag_id = request.query_params.get('tag', None)
        author_id = request.query_params.get('author', None)
        subscribedPosts = request.query_params.get('subscribedPosts', None)
        title = request.query_params.get('title', None)
        filteredPosts = []
        if title is not None:
            posts = posts.filter(title__icontains = title)
        if category_id is not None:
            category = Category.objects.get(pk=category_id)
            posts = posts.filter(category=category)
        if author_id is not None:
            author = RareUser.objects.get(pk=author_id)
            posts = posts.filter(user=author)
        if tag_id is not None:
            tag = Tag.objects.get(pk=tag_id)
            posts = posts.filter(tags=tag)
        if subscribedPosts is not None:
            current_user = RareUser.objects.get(user=request.auth.user)
            subscriptions = Subscription.objects.filter(follower_id=current_user)
            # print(subscriptions)
            for subscription in subscriptions:
                author = RareUser.objects.get(user=subscription.author.id)
                followedPosts = posts.filter(user=author.id)
                for post in followedPosts:
                    post = Post.objects.get(pk=post.id)
                    filteredPosts.append(post)
            posts = filteredPosts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        user = RareUser.objects.get(user=request.auth.user)
        all_tags = []
        tags = request.data["tags"]
        for tag in tags:
            post_tag = Tag.objects.get(pk=tag)
            all_tags.append(post_tag)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, tags=all_tags)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        print(request.data)
        category = Category.objects.get(pk=request.data["category"])
        post.category = category

        all_tags = []
        tags = request.data["tags"]
        for tag in tags:
            post_tag = Tag.objects.get(pk=tag)
            all_tags.append(post_tag)
        post.tags.set(all_tags)
        user = RareUser.objects.get(pk=request.data['user'])
        post.user = user
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



    
        
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content','approved', 'tags')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content','created_on')

class RareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id','full_name')
class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=( 'id','label')


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tag
        fields=( 'id','label')


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    comments=CommentSerializer(many=True)
    user= RareUserSerializer(many=False)
    tags=PostTagSerializer(many=True)
    category = PostCategorySerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content','approved', 'comments', 'tags')
        
        
