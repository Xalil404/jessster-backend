from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'language', 'slug']

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'featured_image', 'excerpt', 
            'content', 'status', 'category', 'language', 'number_of_views',
            'likes_count', 'created_on', 'updated_on'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()
