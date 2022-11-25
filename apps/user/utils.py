import datetime

from django.conf import settings
from django.db.models import Count
from django.utils import timezone

from core.email import send_templated_email
from apps.user.models import Profile


MAX_DAILY_EMAILS_PER_CATEGORY = 10


def send_feedback_email_no_entries():
    """Sends an email to users that didn\'t event create a single entry."""

    now = timezone.now()

    print(f"[{now.strftime('%Y-%M-%d')}] send_feedback_email_no_entries triggered")

    twentyfour_hours_ago = now - datetime.timedelta(hours=24)
    fortyeight_hours_ago = now - datetime.timedelta(hours=48)

    profiles = (
        Profile.objects
        .annotate(
            n_entries=Count('entries'),
        )
        .filter(
            created_sts__gte=fortyeight_hours_ago,
            created_sts__lte=twentyfour_hours_ago,
            feedback_email__isnull=True,
            email_verified_on__isnull=False,
            user__email__isnull=False,
            user__is_active=True,
            n_entries=0,
        )
        .select_related('user')
    )

    profile_count = len(profiles)
    email_count = 0

    for profile in profiles[:10]:
        error = False
        email = profile.user.email

        print(f"Sending 'no_entries' email to {email}")

        try:
            delivered_to = send_templated_email(
                recipients=[email],
                subject='Did you experience problems?',
                from_email=settings.FEEDBACK_FROM_EMAIL,
                text_template='email/feedback/no_entries/email_content.txt',
                html_template='email/feedback/no_entries/email_content.html',
            )
        except Exception:
            error = True

        profile.feedback_email = profile.FEEDBACK_EMAIL_NO_ENTRIES

        if error or len(delivered_to) < 1:
            profile.feedback_email_status = profile.FEEDBACK_EMAIL_STATUS_ERROR
            print(f"Feedback email 'no_entries' could not be delivered to '{email}'.")
        else:
            profile.feedback_email_status = profile.FEEDBACK_EMAIL_STATUS_SENT
            email_count += 1

    Profile.objects.bulk_update(profiles, ['feedback_email', 'feedback_email_status'])

    print(f"{email_count}/{profile_count} 'no_entries' emails sent")


def send_feedback_email_only_one_entry():
    """Sends an email to users that created only one entry."""
    profiles = (
        Profile.objects
            .annotate(num_entries=Count('entries'))
            .filter(num_entries=1)
            .select_related('user')
    )

    for profile in profiles[:MAX_DAILY_EMAILS_PER_CATEGORY]:
        email = profile.user.email
        delivered_to = send_templated_email(
            recipients=[email],
            subject='Feedback',
            from_email=settings.FEEDBACK_FROM_EMAIL,
            text_template='email/feedback/only_one_entries/email_content.txt',
            html_template='email/feedback/only_one_entries/email_content.html',
        )
        if len(delivered_to) < 1:
            print(f"Feedback email 'only_one_entry' could not be delivered to '{email}'.")
