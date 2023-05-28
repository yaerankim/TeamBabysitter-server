from rest_framework import serializers

# from user.models import User # 일단 주석처리
from community.models import Community, Comment

class CommunityCreateSerializer(serializers.ModelSerializer):
    # writer = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Community
        # fields = ['title', 'writer', 'content']
        fields = ['title', 'content', 'category'] # User 일단 주석처리 상태이므로 writer은 field에서 빼기

class CommunityListSerializer(serializers.ModelSerializer):
    # writer = serializers.ReadOnlyField(source='user.nickname')
    comments_count = serializers.SerializerMethodField()
    row_count = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'title', 'created_at', 'view_count', 'comments_count', 'row_count', 'like_count', 'category']

    def get_comments_count(self, obj):
        # community_id -> view에서 comment 등록 관련해서 사용되는 필드
        comments = Comment.objects.filter(community_id=obj.id)
        # comments_count = {
        #         'comments_count':len(comments)
        # }
        comments_count = len(comments)
        return comments_count

    def get_row_count(self, obj):
        community = Community.objects.all()
        row_count = len(community)
        return row_count

class CommunityDetailSerializer(serializers.ModelSerializer):
    # writer = serializers.ReadOnlyField(source='user.nickname')
    comments = serializers.SerializerMethodField()
    row_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField() # 추가

    def get_comments(self, obj):
        comments = [{
                    # 'user':User.objects.get(id=comment.user_id).nickname,
                    'content':comment.content,
                    'created_at':comment.created_at,
                    'updated_at':comment.updated_at,
                } for comment in Comment.objects.filter(community_id=obj.id)]
        return comments

    def get_row_count(self, obj):
        community = Community.objects.all()
        row_count = len(community)
        return row_count
    
    def get_comments_count(self, obj):
        # community_id -> view에서 comment 등록 관련해서 사용되는 필드
        comments = Comment.objects.filter(community_id=obj.id)
        # comments_count = {
        #         'comments_count':len(comments)
        # }
        comments_count = len(comments)
        return comments_count

    class Meta:
        model = Community
        # 해당 필드 순으로 key-value 형태로 response 값 받을 수 있음
        # fields = ['id', 'title', 'writer', 'content', 'view_count', 'updated_at', 'comments']
        fields = ['id', 'title', 'content', 'view_count', 'updated_at', 'comments_count', 'comments', 'row_count', 'like_count', 'category']

class CommentSerializer(serializers.ModelSerializer):
    # writer = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Comment
        # fields = ['id', 'writer', 'content', 'created_at', 'updated_at']
        fields = ['community_id', 'id', 'content', 'created_at', 'updated_at']