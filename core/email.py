import logging
from typing import Dict, List

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def send_templated_email(
    recipients: List = None,
    subject: str = None,
    from_email: str = None,
    text_template: str = None,  # Path
    html_template: str = None,  # Path
    context: Dict = None,
    fail_silently: bool = False,
    **kwargs
) -> List:
    """
    Render email from a text- and html templates and send it natively
    via Django's send_mail() function.
    """
    protocol = 'http' if settings.DEBUG else 'https'
    current_site = Site.objects.get(id=settings.SITE_ID)

    context = context or {}
    context['subject'] = subject
    context['base_url'] = f'{protocol}://{current_site.domain}'

    # Redirect all emails to admins in debug mode.
    # if settings.DEBUG:
    #     to = [entry[1] for entry in settings.ADMINS]

    if not text_template:
        raise Exception('You need to specify a text_template.')

    text_message = render_to_string(text_template, context)
    html_message = render_to_string(html_template, context) if html_template else None

    # NOTE: Looping over recipients and creating an email for each of them
    # is important, passing the list directly to send_mail will only generate
    # one email with all recipients in cc.
    delivered_to = []
    for recipient in recipients:
        try:
            status = send_mail(
                subject,
                text_message,
                from_email or settings.DEFAULT_FROM_EMAIL,
                (recipient,),
                fail_silently=fail_silently,
                html_message=html_message,
                **kwargs,
            )
            # Status equals number of successfully sent emails, can only be 0 or 1.
            if status == 0:
                logger.info(f"send_mail() couldn't deliver '{subject}' email to {recipient}, returned status 0.")
            else:
                delivered_to.append(recipient)
        except Exception:
            logger.error(f"Error in send_mail() when trying to send '{subject}' to {recipient}.")

    return delivered_to
