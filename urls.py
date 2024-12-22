from django.urls import path
from .views import signup, login_view, mainpage, logout_view, create_post, delete_post, profile_view, like_post, add_comment,notifications,menu_view,message_page, group ,delete_friend,accept_friend_request,decline_friend_request,friends_view,send_friend_request

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('mainpage/', mainpage, name='mainpage'),
    path('create_post/', create_post, name='create_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('notifications/', notifications, name='notifications'),
    path('message/', message_page, name='message'),
    path('groups/', group, name='group'),
    path('friends/', friends_view, name='friends'),
    path('friends/delete/<int:friend_id>/', delete_friend, name='delete_friend'),
    path('friends/accept/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('friends/decline/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
    path('friends/send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    # path('groups/', group_list, name='group_list'),
    # path('groups/<int:group_id>/join/', join_group, name='join_group'),
    # path('groups/<int:group_id>/leave/', leave_group, name='leave_group'),
    # path('groups/create/', create_group, name='create_group'),
    path('menu/', menu_view, name='menu'),
]

