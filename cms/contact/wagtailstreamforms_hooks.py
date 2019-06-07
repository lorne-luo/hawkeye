from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.defaultfilters import pluralize

from wagtailstreamforms.hooks import register

@register('process_form_submission')
def email_submission(instance, form):
    """ Send email to admin when user submit. """

    to_addresses = [instance.advanced_settings.to_address]
    from_address = [instance.advanced_settings.from_address]
    subject = 'New Form Submission : %s' % instance.title
    content = ['You have a new submission.\n', ]

    # Creating email content from submission data
    for field in form:
        content.append('{}: {}'.format(field.label, form.cleaned_data[field.name]))
    content = '\n'.join(content)

    # create email 
    email = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_address,
        to=to_addresses
    )

    # send email
    email.send(fail_silently=True)
