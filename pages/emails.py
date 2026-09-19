import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)

BOOKING_TYPES = {
    'ember': {'label': 'Ember Menu', 'noun': 'booking'},
    'fine': {'label': 'Fine Dining', 'noun': 'booking'},
    'casual': {'label': 'Casual Dining', 'noun': 'booking'},
    'custom': {'label': 'Custom Dining', 'noun': 'booking'},
    'hire': {'label': 'Hire a Chef', 'noun': 'request'},
    'contact': {'label': 'Contact Form', 'noun': 'message'},
}

FIELD_LABELS = {
    'your_name': 'Name',
    'phone': 'Phone',
    'email': 'Email',
    'location': 'Location',
    'date': 'Date',
    'time': 'Time',
    'number_of_guest': 'Guests',
    'menu_type': 'Menu Selected',
    'event_type': 'Event Type',
    'subject': 'Subject',
    'message': 'Message',
    'service_details': 'Service Details',
    'bread': 'Bread',
    'side_one': 'Side 1',
    'side_two': 'Side 2',
    'vegetable_one': 'Vegetable 1',
    'vegetable_two': 'Vegetable 2',
    'we_are_allowed_to_take_pictures_of_you_and_your_guest': 'Photos of guests',
    'we_are_allowed_to_take_pictures_of_your_apartment': 'Photos of venue',
    'we_are_allowed_to_use_your_event_content_for_our_business_promotions': 'Use for promotions',
    'additional_information': 'Notes',
}

FIELD_ORDER = [
    'your_name', 'phone', 'email', 'location',
    'date', 'time', 'number_of_guest', 'menu_type', 'event_type',
    'subject', 'message', 'service_details',
    'bread', 'side_one', 'side_two', 'vegetable_one', 'vegetable_two',
    'we_are_allowed_to_take_pictures_of_you_and_your_guest',
    'we_are_allowed_to_take_pictures_of_your_apartment',
    'we_are_allowed_to_use_your_event_content_for_our_business_promotions',
    'additional_information',
]

EXCLUDED_FIELDS = {'captcha'}

CONSENT_FIELDS = {
    'we_are_allowed_to_take_pictures_of_you_and_your_guest',
    'we_are_allowed_to_take_pictures_of_your_apartment',
    'we_are_allowed_to_use_your_event_content_for_our_business_promotions',
}

RECAP_FIELDS = {'menu_type', 'date', 'time', 'number_of_guest'}


def _humanize_value(form, field_name, value):
    """Prefer the model's get_FOO_display() for choice fields (e.g. menu_type -> '3 Course Menu')."""
    display_method = getattr(form.instance, f'get_{field_name}_display', None)
    if callable(display_method):
        return display_method()
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    if value in (None, ''):
        return None
    if hasattr(value, 'strftime'):
        return value.strftime('%d %B %Y') if hasattr(value, 'year') else value.strftime('%I:%M %p').lstrip('0')
    return str(value)


def _ordered_fields(form):
    """Yield (field_name, label, display_value) for every field worth showing, in a sensible order."""
    seen = set()
    ordered_names = FIELD_ORDER + [f for f in form.cleaned_data if f not in FIELD_ORDER]
    for name in ordered_names:
        if name in seen or name in EXCLUDED_FIELDS or name not in form.cleaned_data:
            continue
        seen.add(name)
        value = _humanize_value(form, name, form.cleaned_data[name])
        label = FIELD_LABELS.get(name, name.replace('_', ' ').capitalize())
        yield name, label, value


def _booking_name(form):
    return form.cleaned_data.get('your_name') or form.cleaned_data.get('email') or 'Someone'


def _type_info(dining_type):
    return BOOKING_TYPES.get(dining_type, {'label': dining_type.replace('_', ' ').title(), 'noun': 'booking'})


def _detail_row(label, value):
    return (
        f'<tr><td style="padding:8px 0;border-bottom:1px solid #eee6d8;'
        f'color:#8a8272;font-size:13.5px;">{label}</td>'
        f'<td style="padding:8px 0;border-bottom:1px solid #eee6d8;'
        f'color:#1a1a1a;font-size:13.5px;font-weight:600;text-align:right;">{value}</td></tr>'
    )


def notify_admin(form, dining_type):
    name = _booking_name(form)
    info = _type_info(dining_type)
    subject = f'New {info["noun"].capitalize()}: {info["label"]} — {name}'
    from_email = to = settings.EMAIL_HOST_USER
    email = form.cleaned_data.get('email')

    rows = []
    consent_rows = []
    notes_value = 'No additional notes provided.'
    for field_name, field_label, value in _ordered_fields(form):
        if field_name == 'additional_information':
            if value:
                notes_value = value
            continue
        if field_name in CONSENT_FIELDS:
            consent_rows.append((field_label, value))
        else:
            rows.append((field_label, value if value is not None else '—'))

    details_html = ''.join(_detail_row(l, v) for l, v in rows)
    consent_html = ''.join(
        _detail_row(l, '<span style="color:#1b4332;">&#10003; Allowed</span>' if v == 'Yes'
                    else '<span style="color:#7a1f2b;">Not allowed</span>')
        for l, v in consent_rows
    )
    consent_block = ''
    if consent_html:
        consent_block = (
            '<div style="font-size:11px;font-weight:700;color:#8a8272;text-transform:uppercase;'
            'letter-spacing:.1em;margin-top:20px;margin-bottom:4px;">Consent</div>'
            f'<table style="width:100%;border-collapse:collapse;">{consent_html}</table>'
        )

    reply_button = ''
    if email:
        reply_button = (
            '<div style="padding:8px 32px 24px;">'
            f'<a href="mailto:{email}" style="display:inline-block;background:#ffc107;color:#0a0a0a;'
            'font-weight:700;font-size:14px;padding:13px 26px;border-radius:4px;text-decoration:none;">'
            f'Reply to {name}</a></div>'
        )

    html_content = f"""
    <div style="font-family: Helvetica, Arial, sans-serif; background:#eee6d8; padding:32px;">
      <div style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:8px;overflow:hidden;">
        <div style="background:#0a0a0a;padding:24px 32px;">
          <div style="color:#ffffff;font-weight:800;font-size:15px;letter-spacing:.08em;">OSE DINING</div>
          <div style="color:#ffc107;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;margin-top:6px;">
            New {info['label']} {info['noun'].capitalize()}
          </div>
        </div>
        <div style="padding:24px 32px 4px;">
          <div style="font-size:19px;font-weight:800;color:#1a1a1a;">{name}</div>
        </div>
        <div style="padding:4px 32px;">
          <table style="width:100%;border-collapse:collapse;">{details_html}</table>
          {consent_block}
          <div style="font-size:11px;font-weight:700;color:#8a8272;text-transform:uppercase;letter-spacing:.1em;margin-top:20px;margin-bottom:8px;">Notes</div>
          <div style="font-size:13.5px;color:#8a8272;font-style:italic;padding-bottom:8px;">{notes_value}</div>
        </div>
        {reply_button}
        <div style="border-top:1px solid #eee6d8;padding:16px 32px;font-size:11.5px;color:#b5ac9a;">
          Sent automatically from the booking form on osedining.com.
        </div>
      </div>
    </div>
    """

    text_lines = [f'New {info["label"]} {info["noun"]} from {name}', '']
    text_lines += [f'{l}: {v}' for l, v in rows]
    if consent_rows:
        text_lines.append('')
        text_lines += [f'{l}: {v}' for l, v in consent_rows]
    text_lines += ['', 'Notes:', notes_value]
    text_content = '\n'.join(text_lines)

    reply_to = [email] if email else None
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], reply_to=reply_to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    logger.info('Sent admin notification for %s (%s) to %s', info['label'], name, to)


def notify_user(form, dining_type):
    email = form.cleaned_data.get('email')
    if not email:
        return

    name = _booking_name(form)
    first_name = 'there' if name == 'Someone' or '@' in name else name.split(' ')[0]
    info = _type_info(dining_type)
    noun = 'request' if info['noun'] in ('request', 'message') else 'booking'

    subject = f"We've received your {info['label']} {noun}, {first_name}"

    recap_rows = [
        (label, value) for field_name, label, value in _ordered_fields(form)
        if field_name in RECAP_FIELDS and value
    ]

    recap_html = ''
    if recap_rows:
        rows_html = ''.join(
            '<tr>'
            f'<td style="padding:6px 0;font-size:13.5px;color:#8a8272;">{l}</td>'
            f'<td style="padding:6px 0;font-size:13.5px;color:#1a1a1a;font-weight:600;text-align:right;">{v}</td>'
            '</tr>'
            for l, v in recap_rows
        )
        recap_html = f"""
        <div style="margin:20px 36px 0;background:#f2ede4;border-radius:6px;padding:18px 22px;">
          <div style="font-size:10.5px;font-weight:700;color:#8a8272;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;">Your Request</div>
          <table style="width:100%;border-collapse:collapse;">{rows_html}</table>
        </div>
        """

    html_content = f"""
    <div style="font-family: Helvetica, Arial, sans-serif; background:#eee6d8; padding:32px;">
      <div style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:8px;overflow:hidden;">
        <div style="background:#0a0a0a;padding:28px 36px;">
          <div style="color:#ffffff;font-weight:800;font-size:15px;letter-spacing:.08em;">OSE DINING</div>
        </div>
        <div style="padding:32px 36px 8px;">
          <div style="font-size:22px;font-weight:800;color:#1a1a1a;">Thank you, {first_name}.</div>
          <div style="font-size:14.5px;color:#55503f;line-height:1.6;margin-top:12px;">
            We've received your <strong>{info['label']}</strong> {noun}. Our team will reach out within 24 hours to confirm the details.
          </div>
        </div>
        {recap_html}
        <div style="padding:24px 36px 8px;font-size:13.5px;color:#55503f;line-height:1.6;">
          Have a question in the meantime? Just reply to this email, or reach us directly:
        </div>
        <div style="padding:4px 36px 28px;font-size:13.5px;color:#1a1a1a;line-height:1.9;">
          <strong>+234 816 747 6771</strong><br>
          <strong>ehisfoods@yahoo.com</strong>
        </div>
        <div style="border-top:1px solid #eee6d8;padding:18px 36px;font-size:12.5px;color:#8a8272;">
          Warmly,<br>
          <strong style="color:#1a1a1a;">Chef Ehis</strong> &middot; Ose Private Dining
        </div>
      </div>
    </div>
    """

    text_content = (
        f"Thank you, {first_name}.\n\n"
        f"We've received your {info['label']} {noun}. Our team will reach out within 24 hours to confirm the details.\n\n"
        + (''.join(f'{l}: {v}\n' for l, v in recap_rows) + '\n' if recap_rows else '')
        + "Questions? Reply to this email, or reach us directly:\n"
        "+234 816 747 6771\n"
        "ehisfoods@yahoo.com\n\n"
        "Warmly,\nChef Ehis, Ose Private Dining"
    )

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    logger.info('Sent confirmation email for %s to %s', info['label'], email)


def send_booking_notifications(form, dining_type):
    """Notify the admin and the customer; a failure here never blocks the booking itself."""
    try:
        notify_admin(form, dining_type)
    except Exception:
        logger.exception('Failed to send admin notification for %s', dining_type)

    try:
        notify_user(form, dining_type)
    except Exception:
        logger.exception('Failed to send confirmation email for %s', dining_type)
