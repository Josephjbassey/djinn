from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

def format_html_attrs(attrs):
    """
    Safely format dictionary of attributes into an HTML string.
    Keys with underscores are converted to hyphens.
    Values are HTML-escaped.
    """
    attr_list = []
    for key, value in attrs.items():
        safe_key = key.replace("_", "-")
        # Ensure value is a string before escaping
        safe_value = escape(str(value))
        attr_list.append(f'{safe_key}="{safe_value}"')
    return mark_safe(" ".join(attr_list))

@register.inclusion_tag('components/button.html')
def djinn_button(
    variant="primary",
    size="md",
    disabled=False,
    loading=False,
    label=None,
    class_name="",
    button_type="button",
    icon_left=None,
    icon_right=None,
    **attrs
):
    """
    Djinn Button component tag.
    Usage: {% djinn_button variant="outline" label="Cancel" %}
    """
    return {
        "variant": variant,
        "size": size,
        "disabled": disabled,
        "loading": loading,
        "label": label,
        "class": class_name,
        "type": button_type,
        "icon_left": icon_left,
        "icon_right": icon_right,
        "attrs": format_html_attrs(attrs),
    }
