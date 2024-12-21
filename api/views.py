from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like ,Friend, FriendRequest ,Notification
from .forms import PostForm, CommentForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse
from api.models import Post, Comment, Like, Friend, FriendRequest, Notification
from django.urls import reverse
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

token_generator = PasswordResetTokenGenerator()

def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            print(f"Password for {user.username}: {user.password}")

            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse('reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'your_email@gmail.com',
                [email],
                fail_silently=False,
            )
            print(f"Password reset link sent to {email}: {reset_link}")
            return HttpResponse("A reset link has been sent to your email.")
        except User.DoesNotExist:
            return HttpResponse("This email does not exist in our system.")
    return render(request, 'reset_password_request.html')



def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if token_generator.check_token(user, token): 
            if request.method == 'POST':
                new_password = request.POST.get('password')
                user.set_password(new_password)
                user.save()
                return HttpResponse("Password reset successful.")
            return render(request, 'reset_password_confirm.html', {'valid': True})
        else:
            return render(request, 'reset_password_confirm.html', {'valid': False})  
    except Exception as e:
        return HttpResponse("Invalid link.")



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
from .models import Notification

def login_view(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            unread_notifications_count = Notification.objects.filter(receiver=user, is_read=False).count()
            request.session['unread_notifications_count'] = unread_notifications_count
            return redirect('mainpage')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')



# Main Page
@login_required
def mainpage(request):
    posts = Post.objects.all()
    comment_form = CommentForm()

    unread_notifications_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    request.session['unread_notifications_count'] = unread_notifications_count

    return render(request, 'mainpage.html', {
        'posts': posts,
        'comment_form': comment_form,
    })






# Create Post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            Notification.objects.create(
                type='post', sender=request.user, receiver=request.user, post=post
            )
            return redirect('mainpage')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# Delete Post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
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
    else:
        Notification.objects.create(
            type='like', sender=request.user, receiver=post.user, post=post
        )
    return redirect('mainpage')

# Add Comment
@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            Notification.objects.create(
                type='comment', sender=request.user, receiver=post.user, post=post
            )
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
        post.saved_by.remove(request.user)
        messages.info(request, 'Post unsaved.')
    else:
        post.saved_by.add(request.user)
        messages.success(request, 'Post saved successfully.')
    return redirect('mainpage')

# Saved Posts View
@login_required
def saved_posts(request):
    saved_posts = request.user.saved_posts.all()
    return render(request, 'saved_posts.html', {'saved_posts': saved_posts})

from django.db.models import Count

@login_required
def notifications(request):
    user_posts = Post.objects.filter(user=request.user)
    likes = Like.objects.filter(post__in=user_posts).select_related('user', 'post')
    friend_notifications = Notification.objects.filter(receiver=request.user)

    friend_notifications.update(is_read=True)
    request.session['unread_notifications_count'] = 0

    return render(request, 'notifications.html', {
        'likes': likes,
        'friend_notifications': friend_notifications,
    })



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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def menu_view(request):
    return render(request, 'menu.html')

def user_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)

    return render(request, 'user_profile.html', {
        'profile_user': user,
        'posts': posts,
    })


# view models through APIs using REST Framework.

from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
