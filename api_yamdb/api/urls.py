from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

appname = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', views.UserViewSet, basename='users')
router_v1.register(
    r'categories',
    views.CategoriesViewSet,
    basename='categories'
)
router_v1.register(
    r'genres',
    views.GenresViewSet,
    basename='genres'
)
router_v1.register(
    r'titles',
    views.TitlesViewSet,
    basename='titles'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.register_user, name='register'),
    path('v1/auth/token/', views.get_jwt_token, name='jwt_token')
]
