from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filter import TitleFilter
from .mixins import CreateListDestroy
from .permissions import (OwnerOrModeratorOrAdminOrReadOnly,
                          IsAdminOrReadOnly, Admin)
from .serializers import (UserEditSerializer, RegisterDataSerializer,
                          TokenSerializer, GenresSerializer,
                          UserSerializer, CategoriesSerializer,
                          TitlesCreateSerializer, TitlesReadSerializer,
                          ReviewSerializer, CommentSerializer)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (Admin,)

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        methods=['GET', 'PATCH'],
        url_path='me',
        serializer_class=UserEditSerializer
    )
    def user_profile(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        recipient_list=[user.email],
        from_email=None,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'])
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)},
                        status=status.HTTP_200_OK
                        )
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                    )


class CategoriesViewSet(CreateListDestroy):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlesCreateSerializer
        return TitlesReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrModeratorOrAdminOrReadOnly,)

    def review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
