from .models import Invitation, TransferRequest

def notification_count(request):
    if request.user.is_authenticated:
        # count pending collab invitations
        count = Invitation.objects.filter(
            invited_user=request.user,
            status='pending'
        ).count()

        # count completed transfer requests that haven't been dismissed
        transfer_count = TransferRequest.objects.filter(
            requester=request.user,
            status__in=['APPROVED', 'DENIED'],
            is_notified=False
        ).count()

        # return total unread notifications count
        return {'notification_count': count}
    return {'notification_count': 0}