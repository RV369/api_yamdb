from api.views import UsersApiViewSet, get_sugnup, get_token
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from reviews.views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitleViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register('users', UsersApiViewSet, basename='user')
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

auth_urls = [
    path('auth/signup/', get_sugnup, name='signup'),
    path('auth/token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(auth_urls)),
]
