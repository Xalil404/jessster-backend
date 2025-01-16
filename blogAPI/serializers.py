from rest_framework import serializers
from .models import Post, Category, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'language', 'slug']

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    number_of_views = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()  # Add the field for mobile app

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'featured_image', 'excerpt', 
            'content', 'status', 'category', 'language', 'number_of_views',
            'likes_count', 'comment_count', 'created_on', 'updated_on', 'is_liked'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')  # Get the request from context
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False  # Default to False if the user is not authenticated



class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.ImageField(source='user.profile.profile_picture', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'content', 'created_on', 'updated_on', 'parent_comment', 'username', 'profile_image')
        read_only_fields = ('created_on', 'updated_on', 'user', 'post')

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value










