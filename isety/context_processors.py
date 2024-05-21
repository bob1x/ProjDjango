from .models import Notification
from .models import FriendRequest

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-timestamp')
        friend_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
    else:
        notifications = []
        friend_requests = []
    return {'notifications': notifications, 'friend_requests': friend_requests}

def clear_notifications(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return {'notifications': []}