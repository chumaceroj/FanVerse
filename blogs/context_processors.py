from .models import Invitation, TransferRequest
# importing logical operators (or, and, not)
from django.db.models import Q

def notification_count(request):
    if request.user.is_authenticated:
        # count pending collab invitations
        invitation_count = Invitation.objects.filter(
            invited_user=request.user,
            status='pending'
        ).count()

        # grab all pending transfer requests
        pending_transfer_count = TransferRequest.objects.filter(
            target_user_identifier=request.user.username,
            status='PENDING'
        ).count()

        transfer_status_count = TransferRequest.objects.filter(
            (Q(requester=request.user, requester_notified=False) |
             Q(target_user_identifier=request.user.username, target_notified=False)),
            status__in=['APPROVED', 'DENIED', 'DECLINED', 'JOINED', 'LEFT', 'INVITE_DECLINED']
        ).count()

        # return total unread notifications count
        total_count = invitation_count + pending_transfer_count + transfer_status_count
        return {'notification_count': total_count}
    
    return {'notification_count': 0}