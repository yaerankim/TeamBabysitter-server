from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import CommunityCreateSerializer, CommunityDetailSerializer, CommunityListSerializer
from community.models import Community # , Comment

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

# class CommentCreate(generics.CreateAPIView):
#     queryset= Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def post(self, request, *args, **kwargs):
#         serializer = CommentSerializer(data=request.data)

#         if serializer.is_valid():
#             comment = Comment.objects.create(
#                         user_id = request.user.id,
#                         post_id = self.kwargs['pk'],
#                         content = request.data['content']
#             )
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]