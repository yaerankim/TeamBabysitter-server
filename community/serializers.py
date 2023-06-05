from rest_framework import serializers

# from user.models import User # 일단 주석처리
from community.models import Community, Comment

class CommunityCreateSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='user.nickname') # user명은 읽기 전용으로. 작성자나 관리자가 이후에 수정하지 못하도록.

    class Meta:
        model = Community
        # fields = ['title', 'writer', 'content']
        fields = ['writer', 'title', 'content', 'category'] # User 일단 주석처리 상태이므로 writer은 field에서 빼기

class CommunityListSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='user.nickname')
    comments_count = serializers.SerializerMethodField()
    row_count = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'writer', 'title', 'created_at', 'view_count', 'comments_count', 'row_count', 'like_count', 'category']

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
    writer = serializers.ReadOnlyField(source='user.nickname')
    comments = serializers.SerializerMethodField()
    row_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField() # 추가
    all_comments_count = serializers.SerializerMethodField() # 추가

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
    
    # 모든 comment 총 개수
    def get_all_comments_count(self, obj):
        # community_id -> view에서 comment 등록 관련해서 사용되는 필드
        comments = Comment.objects.all()
        # comments_count = {
        #         'comments_count':len(comments)
        # }
        all_comments_count = len(comments)
        return all_comments_count

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
        fields = ['id', 'writer', 'title', 'content', 'view_count', 'updated_at', 'all_comments_count', 'comments_count', 'comments', 'row_count', 'like_count', 'category']

class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Comment
        # fields = ['id', 'writer', 'content', 'created_at', 'updated_at']
        # fields = ['community_id', 'id', 'writer', 'content', 'created_at', 'updated_at']
        fields = ['community_id', 'id', 'writer', 'content'] # 안드로이드로 comment_get할 경우 date 타입 문제 때문에 주석 처리