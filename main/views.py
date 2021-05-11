from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Types, Post
from .permissions import IsAdminPermission, IsAuthorPermission

from .serializers import TypesSerializer, PostSerializer


class TypesListView(ListAPIView):
    queryset = Types.objects.all()
    serializer_class = TypesSerializer


class PostsListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['types', 'author']
    search_fields = ['title', 'text', 'tags__title']
    ordering_fields = ['created_at', 'title']

    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

