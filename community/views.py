from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import CommunityCreateSerializer, CommunityDetailSerializer, CommunityListSerializer, CommentSerializer
from community.models import Community, Comment

class CommunityCreate(generics.CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunityCreateSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny] # 일단 지금은 AllowAny로 지정

    def post(self, request, *args, **kwargs):
        serializer = CommunityCreateSerializer(data=request.data)

        if serializer.is_valid():
            community = Community.objects.create(
                    # user_id = request.user.id,
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

    # def get(self, request, pk):
    #     serializer = CommunityDetailSerializer(data=request.data)

    #     if serializer.is_valid():
    #         community = community.objects.get(
    #                     # user_id = request.user.id,
    #                     # community_id = self.kwargs['pk'],
    #                     community_id = pk,
    #                     row_count = request.data['row_count'],
    #         )
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommunityList(generics.ListAPIView):
    queryset= Community.objects.all()
    serializer_class = CommunityListSerializer
    permission_classes = [AllowAny]

class CommentCreate(generics.CreateAPIView):
    queryset= Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny] # 일단 지금은 AllowAny로 지정

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = Comment.objects.create(
                        # user_id = request.user.id,
                        community_id = self.kwargs['pk'], # 필드명 수정
                        content = request.data['content']
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny] # 일단 지금은 AllowAny로 지정