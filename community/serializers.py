from rest_framework import serializers

# from user.models import User # 일단 주석처리
from community.models import Community # , Comment

class CommunityCreateSerializer(serializers.ModelSerializer):
    # writer = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Community
        # fields = ['title', 'writer', 'content']
        fields = ['title', 'content'] # User 일단 주석처리 상태이므로 writer은 field에서 빼기

class CommunityListSerializer(serializers.ModelSerializer):
    # writer = serializers.ReadOnlyField(source='user.nickname')
    # comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'title', 'writer', 'created_at', 'view_count'] # , 'comments_count']

    # def get_comments_count(self, obj):
    #     comments = Comment.objects.filter(post_id=obj.id)
    #     comments_count = {
    #             'comments_count':len(comments)
    #     }
    #     return comments_count

class CommunityDetailSerializer(serializers.ModelSerializer):
    # writer = serializers.ReadOnlyField(source='user.nickname')
    # comments = serializers.SerializerMethodField()

    # def get_comments(self, obj):
    #     comments = [{
    #                 'user':User.objects.get(id=comment.user_id).nickname,
    #                 'content':comment.content,
    #                 'created_at':comment.created_at,
    #                 'updated_at':comment.updated_at,
    #             } for comment in Comment.objects.filter(post_id=obj.id)]
    #     return comments

    class Meta:
        model = Community
        # fields = ['id', 'title', 'writer', 'content', 'view_count', 'updated_at', 'comments']
        fields = ['id', 'title', 'content', 'view_count', 'updated_at']

# class CommentSerializer(serializers.ModelSerializer):
#     writer = serializers.ReadOnlyField(source='user.nickname')

#     class Meta:
#         model = Comment
#         fields = ['id', 'writer', 'content', 'created_at', 'updated_at']