from django.urls import path, include
from .views import signup, login_view, mainpage, logout_view, create_post, delete_post, profile_view, like_post, add_comment,notifications,menu_view,delete_friend,accept_friend_request,decline_friend_request,friends_view,send_friend_request ,user_profile_view,like_comment
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikeViewSet 

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('mainpage/', mainpage, name='mainpage'),
    path('create_post/', create_post, name='create_post'),
    path('friends/', friends_view, name='friends'),
    path('friends/delete/<int:friend_id>/', delete_friend, name='delete_friend'),
    path('friends/accept/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('friends/decline/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
    path('friends/send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('profile/<int:user_id>/', user_profile_view, name='user_profile'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('like_comment/<int:comment_id>/', like_comment, name='like_comment'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('notifications/', notifications, name='notifications'),
    path('menu/', menu_view, name='menu'),
    
    path('', include(router.urls)),
]

