from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, User

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    from_user = request.user

    if from_user != to_user and not FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        # Add success message if needed
    return redirect('some-view')  # Redirect to appropriate view


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    
    if friend_request.to_user == request.user:
        request.user.profile.add_friend(friend_request.from_user.profile)
        friend_request.from_user.profile.add_friend(request.user.profile)

        friend_request.delete()
    pass 



@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    
    if friend_request.to_user == request.user:
        friend_request.delete()
        # Add message if needed
    return redirect('some-view')  # Redirect to appropriate view
