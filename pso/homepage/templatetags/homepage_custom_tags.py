from django import template
from datetime import datetime, timedelta, timezone

register = template.Library()

# Returns a True/False specifying whether the date was posted within 24 hours of current time
@register.filter(expects_localtime=True)
def test_if_recent(date):
    current = datetime.now(timezone.utc)
    date_24_hours_from_now = date + timedelta(hours=24)
    return (current <= date_24_hours_from_now)

@register.filter(expects_localtime=True)
def add_24_hours(date):
    return date + timedelta(hours=24)

