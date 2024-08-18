from django.urls import path
from .views import send_friend_request, accept_friend_request, decline_friend_request

urlpatterns = [
    path('send-request/<int:user_id>/', send_friend_request, name='send-friend-request'),
    path('accept-request/<int:request_id>/', accept_friend_request, name='accept-friend-request'),
    path('decline-request/<int:request_id>/', decline_friend_request, name='decline-friend-request'),
]
