from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt

from .serializers import CommunityCreateSerializer, CommunityDetailSerializer, CommunityListSerializer, CommentSerializer
from community.models import Community, Comment
from django.conf import settings

class CommunityCreate(generics.CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunityCreateSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = CommunityCreateSerializer(data=request.data)

        if serializer.is_valid():
            community = Community.objects.create(
                    # user_id = request.user, # request.user.id,
                    title = request.data['title'],
                    content = request.data['content'],
                    view_count = 0,
                    # row_count = Community.objects.all().count(),
            )
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommunityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Community.objects.all()
    serializer_class= CommunityDetailSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]

class CommunityList(generics.ListAPIView):
    queryset= Community.objects.all()
    serializer_class = CommunityListSerializer
    permission_classes = [AllowAny]

class CommentCreate(generics.CreateAPIView):
    queryset= Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = Comment.objects.create(
                        # user_id = request.user,
                        community_id = self.kwargs['pk'], # 필드명 수정
                        content = request.data['content']
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]