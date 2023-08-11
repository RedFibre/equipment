from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from .models import UserActivityLog

@receiver(post_save, sender=Notification)
def delete_old_notifications(sender, instance, **kwargs):
    # Get the count of notifications for the user
    notification_count = Notification.objects.filter(user=instance.user).count()

    if notification_count > 10:
        notifications_to_keep = 5
        notifications_to_delete = notification_count - notifications_to_keep

        oldest_notifications = Notification.objects.filter(user=instance.user).order_by('timestamp')[:notifications_to_delete]

        # Delete each of the oldest notifications
        for notification in oldest_notifications:
            notification.delete()
        
post_save.connect(delete_old_notifications, sender=Notification)

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    # Get the login reason from the custom login form data
    login_reason = request.POST.get('login_reason', 'No Reason')  # You can set a default value or handle empty reason

    # Create UserActivityLog instance for login
    user_activity_log = UserActivityLog.objects.create(user=user, login_time=timezone.now())
    user_activity_log.save()

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    # Retrieve the last UserActivityLog for the user and update the logout time
    user_activity_log = UserActivityLog.objects.filter(user=user).latest('login_time')
    user_activity_log.logout_time = timezone.now()
    user_activity_log.save()