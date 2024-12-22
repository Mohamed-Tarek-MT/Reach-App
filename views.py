from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm

# Sign Up
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Username already exists.')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    return render(request, 'signup.html')

# Login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mainpage')
        else:
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Incorrect password.')
            else:
                messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Main Page
@login_required
def mainpage(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'mainpage.html', {'posts': posts, 'comment_form': comment_form})

# Create Post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('mainpage')
        else:
            return render(request, 'create_post.html', {'form': form})
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# Delete Post
from django.http import HttpResponseForbidden

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('mainpage')

    return render(request, 'delete_post.html', {'post': post})

# Like Post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('mainpage')

# Add Comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect('mainpage')

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# Profile View
@login_required
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = user.posts.all()
    return render(request, 'profile.html', {'user': user, 'posts': posts})

# Save Post
@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.saved_by.filter(id=request.user.id).exists():
        post.saved_by.remove(request.user)  # Remove from saved posts if already saved
        messages.info(request, 'Post unsaved.')
    else:
        post.saved_by.add(request.user)  # Add to saved posts
        messages.success(request, 'Post saved successfully.')
    return redirect('mainpage')

# Saved Posts View
@login_required
def saved_posts(request):
    saved_posts = request.user.saved_posts.all()
    return render(request, 'saved_posts.html', {'saved_posts': saved_posts})


from django.shortcuts import render
from .models import Post, Like

@login_required
def notifications(request):
    # Get all posts by the logged-in user
    user_posts = Post.objects.filter(user=request.user)
    
    # Get all likes on the user's posts
    likes = Like.objects.filter(post__in=user_posts).select_related('user', 'post')
    
    return render(request, 'notifications.html', {'likes': likes})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def menu_view(request):
    return render(request, 'menu.html')




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User

@login_required
def message_page(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')
        reply_to_id = request.POST.get('reply_to')  
        try:
            receiver = User.objects.get(username=receiver_username)
            message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
            if reply_to_id:
                reply_to_message = Message.objects.get(id=reply_to_id)
                reply_to_message.content += f"\n\nReply:\n{message.content}"  
                reply_to_message.save()
            return redirect('message')  
        except User.DoesNotExist:
            return render(request, 'message.html', {'error': 'User does not exist.'})
        except Message.DoesNotExist:
            return render(request, 'message.html', {'error': 'Message does not exist.'})


    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    return render(request, 'message.html', {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
    })


from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages

def group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group_description = request.POST.get('group_description')

        messages.success(request, f'Group "{group_name}" created successfully!')
        return redirect('group_list')

    return render(request, 'group.html')

@login_required
def friends_view(request):
    friends = Friend.objects.filter(user=request.user)
    friend_requests = FriendRequest.objects.filter(receiver=request.user)

    suggestions = User.objects.exclude(
        Q(id__in=friends.values_list('friend_id', flat=True)) |
        Q(id__in=friend_requests.values_list('sender_id', flat=True)) |
        Q(id=request.user.id)
    )

    return render(request, 'friends.html', {
        'friends': friends,
        'friend_requests': friend_requests,
        'suggestions': suggestions,
    })

@login_required
def delete_friend(request, friend_id):
    try:
        friend = Friend.objects.get(user=request.user, friend_id=friend_id)
        friend.delete()  
        reciprocal_friend = Friend.objects.get(user_id=friend_id, friend=request.user)
        reciprocal_friend.delete()

    except Friend.DoesNotExist:
        raise Http404("Friend does not exist.")

    return redirect('friends')

@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
    Friend.objects.create(user=request.user, friend=friend_request.sender)
    Friend.objects.create(user=friend_request.sender, friend=request.user)
    Notification.objects.create(
        type='friend_accept',
        sender=request.user,
        receiver=friend_request.sender
    )

    friend_request.delete()
    return redirect('friends')

@login_required
def decline_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
    friend_request.delete()
    return redirect('friends')

@login_required
def send_friend_request(request, user_id):
    receiver = User.objects.get(id=user_id)
    if not FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        Notification.objects.create(
            type='friend_request',
            sender=request.user,
            receiver=receiver
        )
    return redirect('friends')

from django.shortcuts import render
from .models import Post, Like

@login_required
def notifications(request):

    user_posts = Post.objects.filter(user=request.user)

    likes = Like.objects.filter(post__in=user_posts).select_related('user', 'post')
    
    friend_notifications = Notification.objects.filter(receiver=request.user)
    return render(request, 'notifications.html', {
        'likes': likes,
        'friend_notifications': friend_notifications,
    })

# views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Group
# from .forms import GroupForm

# @login_required
# def group_list(request):
#     groups = Group.objects.all()
#     return render(request, 'group_list.html', {'groups': groups})

# @login_required
# def join_group(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#     group.members.add(request.user)
#     return redirect('group_list')

# @login_required
# def leave_group(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#     group.members.remove(request.user)
#     return redirect('group_list')

# @login_required
# def create_group(request):
#     if request.method == 'POST':
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('group_list')
#     else:
#         form = GroupForm()
#     return render(request, 'create_group.html', {'form': form})



