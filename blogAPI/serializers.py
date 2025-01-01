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

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'featured_image', 'excerpt', 
            'content', 'status', 'category', 'language', 'number_of_views',
            'likes_count', 'created_on', 'updated_on'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on', 'is_approved')
        read_only_fields = ('created_on', 'author')  # Prevent users from changing the author and created_on
