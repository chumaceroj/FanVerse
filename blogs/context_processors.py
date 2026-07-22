from .models import Invitation

def notification_count(request):
    if request.user.is_authenticated:
        count = Invitation.objects.filter(
            invited_user=request.user,
            status='pending'
        ).count()
        return {'notification_count': count}
    return {'notification_count': 0}