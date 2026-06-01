from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

def format_html_attrs(attrs):
    attr_list = []
    for key, value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(value))}"')
    return mark_safe(" ".join(attr_list))

@register.inclusion_tag('components/card.html')
def djinn_card(
    variant="default",
    title=None,
    description=None,
    footer=None,
    slot=None,
    class_name="",
    **attrs
):
    """
    Djinn Card component tag.
    Usage: {% djinn_card title="Card Title" description="Card Description" %}
    """
    return {
        "variant": variant,
        "title": title,
        "description": description,
        "footer": footer,
        "slot": slot,
        "class": class_name,
        "attrs": format_html_attrs(attrs),
    }
